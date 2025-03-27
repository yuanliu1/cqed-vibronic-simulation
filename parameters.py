## Calculates parameters for the simulation based on some base parameters

import numpy as np
import matplotlib.pyplot as plt

# Table 1 Parameters
w_gr = np.array([4.95e13, 4.98e13, 4.92e13])
w_er = np.array([4.63e13, 4.62e13, 4.65e13])
w_l = 6e12
J_AR0 = np.array([3e12, 2.7e12])
n_AR = np.array([-0.1, 0.15])
Sr = np.array([0.005, 0.004, 0.006])
Sl = 0.05
gamma_amp_all = 3.15e12
gamma_dep_all = 9e11

# Table 2 Parameters
w_r = (w_gr + w_er)/2
print(f"omega_r values are: {w_r}")
g_r = np.sqrt(Sr)*w_er
print(f"g_r values are: {g_r}")
g_cdr = g_r * w_gr / w_r
print(f"g_cdr values are: {g_cdr}")
g_cdl = w_l * np.sqrt(Sl)
print(f"g_cdl = {g_cdl}")
chi_r = w_er - w_gr
print(f"chi_r values are: {chi_r}")
omega_qr = w_er*Sr + chi_r/2 + chi_r*g_r**2/(4*(w_r**2)) - g_r**2/w_r
omega_qr[0] += w_l*Sl - g_cdl**2/w_l**2
print(f"omega_qr values are: {omega_qr}")
delta_ar = np.array([omega_qr[0]-omega_qr[1],omega_qr[0]-omega_qr[2]])
print(f"Delta_qr values are: {delta_ar}")