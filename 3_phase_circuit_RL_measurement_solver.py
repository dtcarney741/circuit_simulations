#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 28 10:06:24 2024

@author: david
"""

from sympy import Symbol, nsolve
from tabulate import tabulate

Ru_v_meas = 3.0
Rv_w_meas = 2.1
Rw_u_meas = 5.0

Lu_v_meas = 13.5
Lv_w_meas = 14.3
Lw_u_meas = 27.0


Ru=Symbol('Ru')
Rv=Symbol('Rv')
Rw=Symbol('Rw')

Lu=Symbol('Lu')
Lv=Symbol('Lv')
Lw=Symbol('Lw')

Ruw=Symbol('Ruw')
Rwv=Symbol('Rwv')
Rvu=Symbol('Rvu')

Luw=Symbol('Luw')
Lwv=Symbol('Lwv')
Lvu=Symbol('Lvu')

wye_f1R = Ru + Rw - Rw_u_meas
wye_f2R = Rw + Rv - Rv_w_meas
wye_f3R = Rv + Ru - Ru_v_meas

[wye_Ru, wye_Rv, wye_Rw] = nsolve((wye_f1R, wye_f2R, wye_f3R), (Ru, Rv, Rw), (1,1,1))

wye_f1L = Lu + Lw - Lw_u_meas
wye_f2L = Lw + Lv - Lv_w_meas
wye_f3L = Lv + Lu - Lu_v_meas

[wye_Lu, wye_Lv, wye_Lw] = nsolve((wye_f1L, wye_f2L, wye_f3L), (Lu, Lv, Lw), (1,1,1))

delta_f1R = Ruw*(Rvu + Rwv)/(Ruw + Rvu + Rwv) - Rw_u_meas
delta_f2R = Rwv*(Rvu + Ruw)/(Ruw + Rvu + Rwv) - Rv_w_meas
delta_f3R = Rvu*(Rwv + Ruw)/(Ruw + Rvu + Rwv) - Ru_v_meas

[delta_Ruw, delta_Rwv, delta_Rvu] = nsolve((delta_f1R, delta_f2R, delta_f3R), (Ruw, Rwv, Rvu), (1,1,1))

delta_f1L = Luw*(Lvu + Lwv)/(Luw + Lvu + Lwv) - Lw_u_meas
delta_f2L = Lwv*(Lvu + Luw)/(Luw + Lvu + Lwv) - Lv_w_meas
delta_f3L = Lvu*(Lwv + Luw)/(Luw + Lvu + Lwv) - Lu_v_meas

[delta_Luw, delta_Lwv, delta_Lvu] = nsolve((delta_f1L, delta_f2L, delta_f3L), (Luw, Lwv, Lvu), (1,1,1))

# Create and print the table using tabulate
headers = ["Measurement/\nCalculation", "Measured \nValue (R Ohms)", "Measured \nValue (L mH)", "Wye Configuration \nValue (R Ohms)", "Wye Configuration \nValue (L mH)", "Delta Configuration \nValue (R Ohms)", "Delta Configuration \nValue (L mH)"]
table = [
    ["Ru_v_meas / Lu_v_meas", Ru_v_meas, Lu_v_meas, "", "", "", ""],
    ["Rv_w_meas / Lv_w_meas", Rv_w_meas, Lv_w_meas, "", "", "", ""],
    ["Rw_u_meas / Lw_u_meas", Rw_u_meas, Lw_u_meas, "", "", "", ""],
    ["Ru / Lu", "", "", wye_Ru, wye_Lu, "", ""],
    ["Rv / Lv", "", "", wye_Rv, wye_Lv, "", ""],
    ["Rw / Lw", "", "", wye_Rw, wye_Lw, "", ""],
    ["Ruw / Luw", "", "", "", "", delta_Ruw, delta_Luw],
    ["Rwv / Lwv", "", "", "", "", delta_Rwv, delta_Lwv],
    ["Rvu / Lvu", "", "", "", "", delta_Rvu, delta_Lvu]
]


print(tabulate(table, headers, tablefmt="grid"))
