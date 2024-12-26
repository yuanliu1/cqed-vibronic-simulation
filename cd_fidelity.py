import numpy as np
import matplotlib.pyplot as plt

############################################################
##  Caculates and graphs the range of possible CD error rates
##  based on the CD rate performed and the tunable alpha value
############################################################

## Equation : cd_rate * delta_t = alpha * machine_time * chi

alpha = np.array(range(15,40))            # Testing for a range of alpha
cd_rates = np.array([2.68e12, 1.9e12, 0]) # (/s) Conditional displacement rates (variable)
delta_t = 1e-14                           # (s) The timestep in simulation
chi = 100000*np.pi                        # (/s) The dispersive coupling between two modes
error_rate = 1.6e4                        # (/s) The number of CD errors occuring per second

## Graph labels and colors
labels = ['β=0.0268', 'β=0.019', 'β=0.00']
colors = ['#2f0033', '#4f0056', '#870093']

fidelity = []
for x in range(len(cd_rates)):
    machine_time = (cd_rates[x] * delta_t)/(alpha * chi) # The amount of machine time required to run the gate (s)
    fidelity.append(error_rate * machine_time)
    plt.plot(alpha, fidelity[x], label=labels[x], color=colors[x])
    
plt.fill_between(alpha, fidelity[0], fidelity[2], color='#8b8b8b')


plt.legend(loc=0)
plt.xlabel('α', **{'size':16})
plt.ylabel('Error Probability', **{'size':14})
#plt.yticks([0e-5, 1e-5, 2e-5, 3e-5, 4e-5, 5e-5, 6e-5, 7e-5], fontsize=12)
#plt.xticks(fontsize=12)
plt.axvspan(20, 30, color='red', alpha=0.5)


print("α=20: " + str(fidelity[1][20-15]))
print("α=30: " + str(fidelity[1][30-15]))
plt.show()

