import numpy as np
import matplotlib.pyplot as plt

timestep = 0.01
gamma = 1.15e12/1e12
theta_damp = 2*np.arcsin(np.sqrt(gamma*timestep))

# Ket 0 beginning
alpha_0 = 1
beta_0 = 0

# rotation
theta_rot = np.arange(10 * 12)/12

alpha = alpha_0 * np.cos(theta_rot/2) - beta_0 * np.sin(theta_rot/2)
beta = alpha_0 * np.sin(theta_rot/2) + beta_0 * np.cos(theta_rot/2)

# result of damping
ket_00 = alpha * (np.cos(theta_damp/4) * np.cos(-theta_damp/4) - np.sin(theta_damp/4) * np.sin(-theta_damp/4))
ket_01 = beta * (np.sin(theta_damp/4) * np.cos(-theta_damp/4) - np.cos(theta_damp/4) * np.sin(-theta_damp/4))
ket_10 = beta * (np.sin(theta_damp/4) * np.sin(-theta_damp/4) + np.cos(theta_damp/4) * np.cos(-theta_damp/4))
ket_11 = alpha * (np.cos(theta_damp/4) * np.sin(-theta_damp/4) + np.sin(theta_damp/4) * np.cos(-theta_damp/4))

ket_00 = ket_00 ** 2
ket_01 = ket_01 ** 2
ket_10 = ket_10 ** 2
ket_11 = ket_11 ** 2

plt.plot(theta_rot, ket_00, label = "00")
plt.plot(theta_rot, ket_01, label = "01")
plt.plot(theta_rot, ket_10, label = "10")
plt.plot(theta_rot, ket_11, label = "11")
plt.legend(loc='best')
plt.xlabel("degree of input state (ry rotation)")
plt.ylabel("Probability")
plt.show()