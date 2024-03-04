import numpy as np
from qiskit import *
from qiskit.tools.visualization import plot_histogram
import matplotlib.pyplot as plt
import matplotlib.ticker as tck
import cmath as math



## Constants
delta = .001
l = 10
lmbda_step = .01
lmbda_stop = 1
lmbda = 0

## Calculated Constants
L = 2 * l + 1
gamma = 1 / (np.cos((1/L) * math.acos(1/delta)))
alpha_j = np.zeros(l)
beta_j = np.zeros(l)


## calculate alpha and beta for the range of j
for j in range(1, l + 1):
    alpha_j[j - 1] = (2 * (-1 * np.arctan(np.tan(2 * np.pi * j / L) / math.sqrt(1 - gamma**2)) + (np.pi / 2))).real ## -arctan(x) + pi/2 = cot(x)
    beta_j[l - j ] = alpha_j[j - 1] * -1

one_counts = []
lmbdas = []

sim = Aer.get_backend('aer_simulator')
while lmbda <= lmbda_stop:
    ry_theta = 2 * np.arcsin(np.sqrt(lmbda))
    lmbdas.append(lmbda)
    lmbda += lmbda_step

    qc = QuantumCircuit(1,1)
    qc.ry(ry_theta,0)
    for x in range(l):
        ## St_beta
        qc.p(beta_j[x],0)
        ## Ss_alpha
        qc.ry(ry_theta,0)
        qc.rz(alpha_j[x],0)
        qc.ry(-1 * ry_theta,0)
    qc.measure(0,0)
    counts_qc = execute(qc, sim, shot=1000).result().get_counts()
    if counts_qc.get('1') == None:
        one_counts.append(0)
    else:
        one_counts.append(counts_qc.get('1'))
    
#qc.draw(output="mpl")
#plt.show()


plt.plot(lmbdas, one_counts)
plt.show()


'''
n_qubits = 5
qc = QuantumCircuit(n_qubits + 1, n_qubits)

## querying for 00111
query_string = "00111"


## St(beta)
def st_beta(string, beta):
    qc_st_beta = QuantumCircuit(n_qubits + 1)
    string_length = len(string)
    ## Oracle
    for x in range(1, string_length + 1):
        if string[x-1] == '1':
            qc_st_beta.cnot(string_length - x, string_length)

    qc_st_beta.rz(beta, n_qubits)
    ## Oracle
    for x in range(1, string_length + 1):
        if string[x-1] == '1':
            qc_st_beta.cnot(string_length - x, string_length)
    qc_st_beta.draw(output="mpl")
    plt.show()
    return qc_st_beta


qc.append(st_beta(query_string, beta_j[1]).to_instruction(), range(n_qubits + 1)), 
'''