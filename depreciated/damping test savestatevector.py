import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace
import qiskit_aer
import numpy as np
import matplotlib.pyplot as plt
import c2qa
import c2qa.util as util
import c2qa.util
from qiskit_aer.library import SaveDensityMatrix

# Simulation Parameters
timestep = 0.01
steps = 201
time = np.round(np.arange(steps) * timestep, 5)

# Data values
gamma = np.array([1.15e12/1e12, 1.45e12/1e12])
gamma = gamma
theta_damp = 2*np.arcsin(np.sqrt(gamma*timestep)) 
# damping probability: omega = sin^2(theta/2) = gamma * delta_t (believe is timestep / trotter step)
# damping probability

lambda_t = np.array([4, 6]) * timestep

theta_motion = np.array([360, 360]) * timestep


# Stored Data
rho_A = []
rho_B = []
qumode_A = []
qumode_B = []
counts_00 = []
counts_01 = []
counts_10 = []
counts_11 = []


qumode_reg = c2qa.QumodeRegister(num_qumodes=2, num_qubits_per_qumode=2)
data_reg = QuantumRegister(4)
classical_reg = ClassicalRegister(2)
circuit = c2qa.CVCircuit(qumode_reg, data_reg, classical_reg)

circuit.x(data_reg[0])
lambda_c = lambda_t * 1.0
theta_motion_c = theta_motion * 1.0

for current_time in time:
    print('Time: {:.2f}'.format(current_time))
    
    # Initialize Circuit

    circuit.ry(theta_motion_c[0]/2, data_reg[0])
    circuit.ry(theta_motion_c[1]/2, data_reg[1])
    circuit.cx(data_reg[0], data_reg[1])
    
    circuit.cv_c_d(lambda_c[0]/2, qumode_reg[0], data_reg[0])
    circuit.cv_c_d(lambda_c[1]/2, qumode_reg[1], data_reg[1])

    
    circuit.cv_c_d(lambda_c[1]/2, qumode_reg[1], data_reg[1])
    circuit.cv_c_d(lambda_c[0]/2, qumode_reg[0], data_reg[0])
    circuit.cx(data_reg[0], data_reg[1])
    circuit.ry(theta_motion_c[1]/2, data_reg[1])
    circuit.ry(theta_motion_c[0]/2, data_reg[0])
    

#    for bit_idx in range(2):
#        ancilla_idx = bit_idx + 2
#        circuit.ry(-theta_damp[bit_idx], data_reg[ancilla_idx])
#        circuit.z(data_reg[ancilla_idx])
#        circuit.cz(data_reg[bit_idx], data_reg[ancilla_idx])

    save_densitymatrix = SaveDensityMatrix(1, label='densitymatrix_a{}'.format(current_time))
    circuit.append(save_densitymatrix, [data_reg[0]])
    save_densitymatrix = SaveDensityMatrix(1, label='densitymatrix_b{}'.format(current_time))
    circuit.append(save_densitymatrix, [data_reg[1]])
       

stateop, result, _ = c2qa.util.simulate(circuit)
data = result.data()


for current_time in time:
    rho_A.append(np.asarray(data['densitymatrix_a{}'.format(current_time)])[1,1])
    rho_B.append(np.asarray(data['densitymatrix_b{}'.format(current_time)])[1,1])

#    try:
#        counts_00.append(counts['00'])
#    except Exception:
#        counts_00.append(0)
#    try:
#       counts_01.append(counts['01'])
#    except Exception:
#        counts_01.append(0)
#    try:
#        counts_10.append(counts['10'])
#    except Exception:
#        counts_10.append(0)
#    try:
#        counts_11.append(counts['11'])
#    except Exception:
#        counts_11.append(0)
    
#counts_00 = np.array(counts_00) / 1024
#counts_01 = np.array(counts_01) / 1024
#counts_10 = np.array(counts_10) / 1024
#counts_11 = np.array(counts_11) / 1024
#print(rho_A)
#print(rho_B)
#rint(counts_00)
plt.plot(time, rho_A, label="qubit A")
plt.plot(time, rho_B, label="qubit B")
#plt.plot(time, qubit_A, label="mode A")
#plt.plot(time, qubit_B, label="mode B")
#plt.plot(time, counts_00, label='00')
#plt.plot(time, counts_01, label='01')
#plt.plot(time, counts_10, label='10')
#plt.plot(time, counts_11, label='11')
plt.legend(loc="best")
plt.show()

#circuit.draw(output='mpl')
#plt.show()