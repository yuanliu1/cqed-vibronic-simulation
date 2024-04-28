from qiskit import QuantumCircuit
import c2qa

qmr_test = c2qa.QumodeRegister(4, num_qubits_per_qumode = 1)
circuit_test = c2qa.CVCircuit(qmr_test)

circuit_test.cv_r(-4.79e12,qmr_test[0])
circuit_test.cv_r(-4.8e12,qmr_test[1])
circuit_test.cv_r(-4.79e12,qmr_test[2])
circuit_test.cv_r(-6e11,qmr_test[3])

