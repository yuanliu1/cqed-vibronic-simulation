import numpy as np
import matplotlib.pyplot as plt

# Equation : cd_rate * delta_t = alpha * machine_time * chi
#testing for a range of alpha
alpha = np.array(range(15,40))
#Conditional displacement (/s)
cd_rate = 1.9e12
# (s) The timestep in simulation
delta_t = 1e-14
#(/s)
chi = 100000*np.pi
#(s)
machine_time = (cd_rate * delta_t)/(alpha * chi)

#plt.plot(alpha, machine_time)
#plt.show()

#(/s)
error_rate = 1.6e4
fidelity = error_rate * machine_time

plt.plot(alpha, fidelity, color='#2f0033')

plt.xlabel('α', **{'size':16})
plt.ylabel('Error Probability', **{'size':14})
plt.yticks([0e-5, 1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5, 7e-5], fontsize=12)
plt.xticks(fontsize=12)
plt.axvspan(20, 30, color='red', alpha=0.5)
#plt.grid()

print("α=20: " + str(fidelity[20-15]))
print("α=30: " + str(fidelity[30-15]))
plt.show()

