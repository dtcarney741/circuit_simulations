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
RU_W_VAL = 5
RW_V_VAL = 5
RV_U_VAL = 5
LU_W_VAL = 220
LW_V_VAL = 220
LV_U_VAL = 220

circuit = Circuit('Three Phase Motor - Delta')

# Define three independent voltage sources
circuit.SinusoidalVoltageSource(1, 'N001', circuit.gnd, amplitude=VSRC @ u_V, frequency=FREQUENCY @ u_Hz)
circuit.SinusoidalVoltageSource(2, 'N002', circuit.gnd, amplitude=VSRC @ u_V, frequency=FREQUENCY @ u_Hz, delay=1/(3*FREQUENCY) @u_s)
circuit.SinusoidalVoltageSource(3, 'N003', circuit.gnd, amplitude=VSRC @ u_V, frequency=FREQUENCY @ u_Hz, delay=2/(3*FREQUENCY) @u_s)

# Define the three phases of the motor
circuit.R('UW', 'N001', 'N004', RU_W_VAL @ u_Ohm)
circuit.R('WV', 'N002', 'N005', RW_V_VAL @ u_Ohm)
circuit.R('VU', 'N003', 'N006', RV_U_VAL @ u_Ohm)

# Connect motor windings (assuming star configuration)
circuit.L('UW', 'N004', 'N002', LU_W_VAL @ u_mH)
circuit.L('WV', 'N005', 'N003', LW_V_VAL @ u_mH)
circuit.L('VU', 'N006', 'N001', LV_U_VAL @ u_mH)


# Define the simulation
simulator = circuit.simulator(temperature=25, nominal_temperature=25)
analysis = simulator.transient(step_time=1 @ u_ms, end_time=500 @ u_ms)

node1_voltage = np.array(analysis['N001'])
node2_voltage = np.array(analysis['N002'])
node3_voltage = np.array(analysis['N003'])

LU_W_current = np.array(analysis['LUW'])
LW_V_current = np.array(analysis['LWV'])
LV_U_current = np.array(analysis['LVU'])


# Plot the results
fig1 = plt.figure()
plt.plot(np.array(analysis.time), node1_voltage, label='V(N001)')
plt.plot(np.array(analysis.time), node2_voltage, label='V(N002)')
plt.plot(np.array(analysis.time), node3_voltage, label='V(N003)')
plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Voltage (V)")
plt.show()

fig2 = plt.figure()
plt.plot(np.array(analysis.time), LU_W_current, label='LU_W current')
plt.plot(np.array(analysis.time), LW_V_current, label='LW_V current')
plt.plot(np.array(analysis.time), LV_U_current, label='LV_U current')

plt.legend()
plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
plt.show()
