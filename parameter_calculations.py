import numpy as np

#standard parameters
omega_ga = 4.95e13
omega_ea = 4.63e13
omega_gb = 4.98e13
omega_eb = 4.62e13
omega_gc = 4.92e13
omega_ec = 4.65e13
omega_l = 6.00e12
J_AB_0 = 3.00e12
J_AC_0 = 2.70e12
eta_AB = -0.1
eta_AC = 0.15
S_a = 0.005
S_b = 0.004
S_c = 0.006
S_l = 0.05 #tunable
gamma_A = 3.15e12
gamma_B = 3.15e12
gamma_C = 3.15e12

# Parameter conversion
omega_a = (omega_ga + omega_ea)/2
omega_b = (omega_gb + omega_eb)/2
omega_c = (omega_gc + omega_ec)/2
omega_l = omega_l
chi_a = omega_ea - omega_ga
chi_b = omega_eb - omega_gb
chi_c = omega_ec - omega_gc
omega_qa = 2 * (S_a * omega_ea + S_l * omega_l) + (chi_a) / 2
omega_qb = 2 * S_b * omega_eb + (chi_b) / 2
omega_qc = 2 * S_c * omega_ec + (chi_c) / 2
g_cd_a = np.sqrt(2 * S_a) * omega_ea
g_cd_b = np.sqrt(2 * S_b) * omega_eb
g_cd_c = np.sqrt(2 * S_c) * omega_ec
g_cd_l = np.sqrt(2 * S_l) * omega_l
g_ab = J_AB_0
g_ac = J_AC_0
g_abl = g_ab * eta_AB
g_acl = g_ac * eta_AC
g_a = g_cd_a / 2
g_b = g_cd_b / 2
g_c = g_cd_c / 2
g_l = g_cd_l / 2
delta_ab = omega_qa - omega_qb
delta_ac = omega_qa - omega_qc

# Parameter output
print("omega_a: " + '{:.4e}'.format(omega_a))
print("omega_b: " + '{:.4e}'.format(omega_b))
print("omega_c: " + '{:.4e}'.format(omega_c))
print("omega_l: " + '{:.4e}'.format(omega_l))
print("omega_qa: " + '{:.4e}'.format(omega_qa))
print("omega_qb: " + '{:.4e}'.format(omega_qb))
print("omega_qc: " + '{:.4e}'.format(omega_qc))
print("chi_a: " + '{:.4e}'.format(chi_a))
print("chi_b: " + '{:.4e}'.format(chi_b))
print("chi_c: " + '{:.4e}'.format(chi_c))
print("g_cd_a: " + '{:.4e}'.format(g_cd_a))
print("g_cd_b: " + '{:.4e}'.format(g_cd_b))
print("g_cd_c: " + '{:.4e}'.format(g_cd_c))
print("g_cd_l: " + '{:.4e}'.format(g_cd_l))
print("g_ab: " + '{:.4e}'.format(g_ab))
print("g_ac: " + '{:.4e}'.format(g_ac))
print("g_abl: " + '{:.4e}'.format(g_abl))
print("g_acl: " + '{:.4e}'.format(g_acl))
print("g_a: " + '{:.4e}'.format(g_a))
print("g_b: " + '{:.4e}'.format(g_b))
print("g_c: " + '{:.4e}'.format(g_c))
print("g_l: " + '{:.4e}'.format(g_l))
print("delta_ab: " + '{:.4e}'.format(delta_ab))
print("delta_ac: " + '{:.4e}'.format(delta_ac))