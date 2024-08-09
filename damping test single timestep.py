import qiskit
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.quantum_info import Statevector, DensityMatrix, partial_trace
import qiskit_aer
import numpy as np
import matplotlib.pyplot as plt
import c2qa
import c2qa.util as util
import c2qa.util
import matplotlib.pyplot as plt

# Simulation Parameters
timestep = 0.01
steps = 101
time = [0.1]
trotter_steps = 1

# Data values
gamma = np.array([1.15e13/1e12, 3.45e13/1e12])
gamma = gamma / trotter_steps
theta_damp = 2*np.arcsin(np.sqrt(gamma*timestep))

lambda_t = np.array([4, 6]) * timestep / trotter_steps

theta_motion = np.array([360, 360]) * timestep / trotter_steps


# Stored Data
rho_A = []
rho_B = []
qubit_A = []
qubit_B = []
counts_00 = []
counts_01 = []
counts_10 = []
counts_11 = []

for current_time in time:
    print('Time: {:.2f}'.format(current_time))
    # Initialize Circuit
    qumode_reg = c2qa.QumodeRegister(num_qumodes=2, num_qubits_per_qumode=2)
    data_reg = QuantumRegister(2)
    ancilla_reg = QuantumRegister(2)
    classical_reg = ClassicalRegister(2)
    circuit = c2qa.CVCircuit(qumode_reg, data_reg, ancilla_reg, classical_reg)

    lambda_c = lambda_t * current_time
    theta_motion_c = theta_motion * current_time

    circuit.x(data_reg[0])
    for trotter_step in range(trotter_steps):
        circuit.ry(theta_motion_c[0], data_reg[0])
        circuit.ry(theta_motion_c[1], data_reg[1])
        circuit.cx(data_reg[0], data_reg[1])
        circuit.cv_c_d(lambda_c[0], qumode_reg[0], data_reg[0])
        circuit.cv_c_d(lambda_c[1], qumode_reg[1], data_reg[1])
        circuit.cv_r(5, qumode_reg[0])
        circuit.draw(output="mpl")
        plt.show()
        for bit_idx in range(2):
            circuit.ry(theta_damp[bit_idx]/2, ancilla_reg[bit_idx])
            circuit.cx(data_reg[bit_idx], ancilla_reg[bit_idx])
            circuit.ry(-theta_damp[bit_idx]/2, ancilla_reg[bit_idx])
            circuit.cx(data_reg[bit_idx], ancilla_reg[bit_idx])
            circuit.cx(ancilla_reg[bit_idx], data_reg[bit_idx])
            circuit.measure(ancilla_reg[bit_idx], classical_reg[bit_idx])
        #circuit.reset(ancilla_reg)

    stateop, result, _ = c2qa.util.simulate(circuit)
    density_matrix = DensityMatrix(np.asarray(c2qa.util.trace_out_qumodes(circuit, stateop)))
    #partial_trace(density_matrix, [1,2,3])
    print(np.asarray(partial_trace(density_matrix, [1,2,3])))
    print(np.asarray(partial_trace(density_matrix, [0,1,3])))

    counts = result.get_counts()
