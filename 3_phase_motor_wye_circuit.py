#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec 23 19:39:16 2024

@author: david
"""
import numpy as np
import matplotlib.pyplot as plt

import PySpice.Logging.Logging as Logging
logger = Logging.setup_logging()

from PySpice.Probe.Plot import plot
from PySpice.Spice.Library import SpiceLibrary
from PySpice.Spice.Netlist import Circuit
from PySpice.Unit import *

# Circuit Simulation Inputs
FREQUENCY = 60
VSRC = np.sqrt(2) * 120
RU_VAL = 5
RV_VAL = 5
RW_VAL = 5
LU_VAL = 125
LV_VAL = 125
LW_VAL = 125

circuit = Circuit('Three Phase Motor - Wye')

# Define three independent voltage sources
circuit.SinusoidalVoltageSource(1, 'N001', circuit.gnd, amplitude=VSRC @ u_V, frequency=FREQUENCY @ u_Hz)
circuit.SinusoidalVoltageSource(2, 'N002', circuit.gnd, amplitude=VSRC @ u_V, frequency=FREQUENCY @ u_Hz, delay=1/(3*FREQUENCY) @u_s)
circuit.SinusoidalVoltageSource(3, 'N003', circuit.gnd, amplitude=VSRC @ u_V, frequency=FREQUENCY @ u_Hz, delay=2/(3*FREQUENCY) @u_s)

# Define the three phases of the motor
circuit.R('U', 'N001', 'N004', RU_VAL @ u_Ohm)
circuit.R('V', 'N002', 'N005', RV_VAL @ u_Ohm)
circuit.R('W', 'N003', 'N006', RW_VAL @ u_Ohm)

# Connect motor windings (assuming star configuration)
circuit.L('U', 'N004', 'N007', LU_VAL @ u_mH)
circuit.L('V', 'N005', 'N007', LV_VAL @ u_mH)
circuit.L('W', 'N006', 'N007', LW_VAL @ u_mH)

# Ground connection for the neutral point
#circuit.R(4, 'N007', circuit.gnd, 1 @ u_Ohm)

# Define the simulation
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=1 @ u_ms, end_time=500 @ u_ms)

node1_voltage = np.array(analysis['N001'])
node2_voltage = np.array(analysis['N002'])
node3_voltage = np.array(analysis['N003'])
node7_voltage = np.array(analysis['N007'])

LU_current = np.array(analysis['LU'])
LV_current = np.array(analysis['LV'])
LW_current = np.array(analysis['LW'])


# Plot the results
fig1 = plt.figure()
plt.plot(np.array(analysis.time), node1_voltage, label='V(N001)')
plt.plot(np.array(analysis.time), node2_voltage, label='V(N002)')
plt.plot(np.array(analysis.time), node3_voltage, label='V(N003)')
plt.plot(np.array(analysis.time), node7_voltage, label='V(N007)')
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.show()

fig2 = plt.figure()
plt.plot(np.array(analysis.time), LU_current, label='LU current')
plt.plot(np.array(analysis.time), LV_current, label='LV current')
plt.plot(np.array(analysis.time), LW_current, label='LW current')

plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
plt.show()
