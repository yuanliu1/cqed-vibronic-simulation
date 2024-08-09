# The C2QA pacakge is currently not published to PyPI.
# To use the package locally, add the C2QA repository's root folder to the path prior to importing c2qa.
import os
import sys
# module_path = os.path.abspath(os.path.join("../.."))
module_path = os.path.abspath(os.path.join("../../"))
if module_path not in sys.path:
    sys.path.append(module_path)

# Cheat to get MS Visual Studio Code Jupyter server to recognize Python venv
module_path = os.path.abspath(os.path.join("../../venv/Lib/site-packages"))
if module_path not in sys.path:
    sys.path.append(module_path)

import c2qa
import qiskit
import numpy as np
import c2qa.util as util
import matplotlib.pyplot as plt
import matplotlib
import scipy.sparse.linalg as LA
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister, transpile

output_name = "test"
#output_name = sys.argv[1]

## This is the TEST part, only need to run once
qmr_test = c2qa.QumodeRegister(4, num_qubits_per_qumode = 1)
circuit_test = c2qa.CVCircuit(qmr_test)

circuit_test.cv_r(-4.79e12,qmr_test[0])
circuit_test.cv_r(-4.8e12,qmr_test[1])
circuit_test.cv_r(-4.79e12,qmr_test[2])
circuit_test.cv_r(-6e11,qmr_test[3])

_, result, _ = c2qa.util.simulate(circuit_test)

# Global parameters
omega = np.array([4.79e13, 4.8e13, 4.785e13, 6e12])/1e12 #omega_a,b,c,l
# omega_q = np.array([-1.14e12, -1.43e12, -7.92e11])/1e12 #omega_qb,qb,qc
delta_qa = np.array([8.934e11, 2.55e11])/1e12 #delta_ab,ac
chi = np.array([-3.2e12, -3.6e12, -2.7e12])/1e12 #chi_a,b,c
g_cd = np.array([4.63e12, 4.1323e12, 5.0938e12])/1e12 #g_cda,cdb,cdc
g_cdl = (1.8974e12+0.0j)/1e12 #g_cdl
g_a = np.array([3e12, 2.7e12])/1e12 #g_ab,ac
g_al = np.array([-3e11, 4.05e11])/1e12 #g_abl,acl

# Circuit initialize
global numberofmodes, numberofqubitspermode, cutoff
numberofmodes=4
numberofqubitspermode=2
cutoff=2**numberofqubitspermode

def initialize_circuit():
    qmr = c2qa.QumodeRegister(num_qumodes=numberofmodes, num_qubits_per_qumode=numberofqubitspermode)
    qbr = QuantumRegister(size = 2*numberofmodes)
    circuit = c2qa.CVCircuit(qmr, qbr)
    return qmr, qbr, circuit

# Build circuit for exp(-iH_0*tau) Needs trotterization.
def H0(tau, omega_list=omega, delta_list=delta_qa, reverse = False):
    omega_t = -tau*omega_list
    delta_t = -tau*delta_list
    if not reverse:
        for i_qumode in range(numberofmodes):
            circuit.cv_r(omega_t[i_qumode], qmr[i_qumode])
        for i_qumode in range(1,numberofmodes-1):
            circuit.rz(delta_t[i_qumode-1], qbr[i_qumode])
    else:
        for i_qumode in range(1,numberofmodes-1):
            circuit.rz(delta_t[i_qumode-1], qbr[i_qumode])
        for i_qumode in range(numberofmodes):
            circuit.cv_r(omega_t[i_qumode], qmr[i_qumode])
    circuit.barrier()

# Build circuit for exp(-iH_1*tau)
def H1(tau, chi_list = chi, g_cd_list = g_cd, reverse = False):
    chi_t = tau*chi_list/(2)
    g_cdt = tau*g_cd_list/(2)*1j
    if not reverse:
        for i_qumode in range(numberofmodes-1):
            circuit.cv_c_r(chi_t[i_qumode], qmr[i_qumode], qbr[i_qumode])
            circuit.cv_c_d(g_cdt[i_qumode], qmr[i_qumode], qbr[i_qumode])
    else:
        for i_qumode in range(numberofmodes-1):
            r_i_qumode = numberofmodes-2-i_qumode #reverse index
            circuit.cv_c_d(g_cdt[r_i_qumode], qmr[r_i_qumode], qbr[r_i_qumode])
            circuit.cv_c_r(chi_t[r_i_qumode], qmr[r_i_qumode], qbr[r_i_qumode])
    circuit.barrier()

# Build circuit for exp(-iH_2*tau) Rotated version: Split H2XX and H2YY
def H2XX(tau, g_cdl=g_cdl, g_a_list=g_a, g_al_list=g_al, reverse = False):
    g_at = 2*tau*g_a_list
    g_alt = -1j*tau*g_al_list
    if not reverse:
        for i_qumode in range(2): # ab and ac
            circuit.rxx(g_at[i_qumode]/2, qbr[0], qbr[1+i_qumode])
    
        # Displaced qb for l controlled by sigma_a^x
        circuit.swap(qbr[0], qbr[3])
        circuit.cv_c_d(1j*g_cdl*tau/(4), qmr[3], qbr[3])
        circuit.swap(qbr[0], qbr[3])
        circuit.barrier()
    
        # Displaced qb for l controlle by sigma_a^x*sigma_(b or c)^x
        for i_qumode in range(1,3):
            circuit.h(qbr[0])
            circuit.h(qbr[i_qumode])
            circuit.cx(qbr[i_qumode], qbr[0])
            circuit.swap(qbr[0], qbr[3])
            circuit.cv_c_d(g_alt[i_qumode-1]/2, qmr[3], qbr[3])
            circuit.swap(qbr[0], qbr[3])
            circuit.cx(qbr[i_qumode], qbr[0])
            circuit.h(qbr[0])
            circuit.h(qbr[i_qumode])
            circuit.barrier()
    else:
        # Displaced qb for l controlle by sigma_a^x*sigma_(b or c)^x
        for i_qumode in range(1,3):
            r_i_qumode = numberofmodes-1-i_qumode # reverse index
            circuit.h(qbr[0])
            circuit.h(qbr[r_i_qumode])
            circuit.cx(qbr[r_i_qumode], qbr[0])
            circuit.swap(qbr[0], qbr[3])
            circuit.cv_c_d(g_alt[-i_qumode]/2, qmr[3], qbr[3])
            circuit.swap(qbr[0], qbr[3])
            circuit.cx(qbr[r_i_qumode], qbr[0])
            circuit.h(qbr[0])
            circuit.h(qbr[r_i_qumode])
            circuit.barrier()
        
        # Displaced qb for l controlled by sigma_a^x
        circuit.swap(qbr[0], qbr[3])
        circuit.cv_c_d(1j*g_cdl*tau/(4), qmr[3], qbr[3])
        circuit.swap(qbr[0], qbr[3])
        circuit.barrier()
        
        for i_qumode in range(2): # ab and ac
            r_i_qumode = 1-i_qumode # reverse index
            circuit.rxx(g_at[-i_qumode-1]/2, qbr[0], qbr[1+r_i_qumode])

def H2YY(tau, g_cdl=g_cdl, g_a_list=g_a, g_al_list=g_al, reverse = False):
    g_at = tau*g_a_list
    g_alt = -1j*tau*g_al_list
    if not reverse:
        for i_qumode in range(2): # ab and ac
            circuit.ryy(g_at[i_qumode], qbr[0], qbr[1+i_qumode])
    
        # Displaced qb for l controlled by sigma_a^x
        circuit.swap(qbr[0], qbr[3])
        circuit.cv_c_d(1j*g_cdl*tau/(4), qmr[3], qbr[3])
        circuit.swap(qbr[0], qbr[3])
        circuit.barrier()
    
        # Displaced qb for l controlle by sigma_a^x*sigma_(b or c)^x
        for i_qumode in range(1,3):
            circuit.rz(-np.pi/2,qbr[0])
            circuit.h(qbr[0])
            circuit.rz(-np.pi/2,qbr[i_qumode])
            circuit.h(qbr[i_qumode])
            circuit.cx(qbr[i_qumode], qbr[0])
            circuit.swap(qbr[0], qbr[3])
            circuit.cv_c_d(g_alt[i_qumode-1]/2, qmr[3], qbr[3])
            circuit.swap(qbr[0], qbr[3])
            circuit.cx(qbr[i_qumode], qbr[0])
            circuit.h(qbr[0])
            circuit.rz(np.pi/2,qbr[0])
            circuit.h(qbr[i_qumode])
            circuit.rz(np.pi/2,qbr[i_qumode])
            circuit.barrier()
    else:
        # Displaced qb for l controlle by sigma_a^x*sigma_(b or c)^x
        for i_qumode in range(1,3):
            r_i_qumode = numberofmodes-1-i_qumode # reverse index
            circuit.rz(np.pi/2,qbr[0])
            circuit.h(qbr[0])
            circuit.rz(np.pi/2,qbr[r_i_qumode])
            circuit.h(qbr[r_i_qumode])
            circuit.cx(qbr[r_i_qumode], qbr[0])
            circuit.swap(qbr[0], qbr[3])
            circuit.cv_c_d(g_alt[-i_qumode]/2, qmr[3], qbr[3])
            circuit.swap(qbr[0], qbr[3])
            circuit.cx(qbr[r_i_qumode], qbr[0])
            circuit.h(qbr[0])
            circuit.rz(-np.pi/2,qbr[0])
            circuit.h(qbr[r_i_qumode])
            circuit.rz(-np.pi/2,qbr[r_i_qumode])
            circuit.barrier()
        
        # Displaced qb for l controlled by sigma_a^x
        circuit.swap(qbr[0], qbr[3])
        circuit.cv_c_d(1j*g_cdl*tau/(4), qmr[3], qbr[3])
        circuit.swap(qbr[0], qbr[3])
        circuit.barrier()
        
        for i_qumode in range(2): # ab and ac
            r_i_qumode = 1-i_qumode # reverse index
            circuit.ryy(g_at[-i_qumode-1]/2, qbr[0], qbr[1+r_i_qumode])

# Build circuit and do loop
from qiskit.quantum_info import DensityMatrix, partial_trace
from tqdm import tqdm

rho_A = []
rho_B = []
rho_C = []
sim_steps = 200
tau = 0
timestep = 0.01

# Damping phase so damping probability is sin(theta/2)^2 = (gamma_all*timestep)^2
gamma = np.array([3.15e12/1e12, 9.45e12/1e12, 1.05e12/1e12, 3.15e12/1e12]) # gamma_a/max
theta = 2*np.arcsin(np.sqrt(gamma*timestep))

time = np.round(np.arange(sim_steps)*timestep, 5)

for i in tqdm(range(sim_steps)):
    if i%1 == 0:
        print('\nTime: {}'.format(time[i]))
    tau = time[i]
    
    circuit = 0 # reinitialize circuit

    qmr, qbr, circuit = initialize_circuit()
    circuit.x(qbr[0])
    print("Steps: " + str(i))
    for i_steps in range(i):
        H0(timestep/2)
        H1(timestep/2)
        H2XX(timestep/2)
        H2YY(timestep/2)
        H2YY(timestep/2, reverse = True)
        H2XX(timestep/2, reverse = True)
        H1(timestep/2, reverse = True)
        H0(timestep/2, reverse = True)
        # Now include damping from https://arxiv.org/pdf/2302.14592.pdf (Fig 8)
        #circuit.reset(qbr[numberofmodes:2*numberofmodes])
        #for idx_qb in range(numberofmodes):
        #    idx_damp = idx_qb + numberofmodes
        #    circuit.ry(theta[idx_qb]/2, qbr[idx_damp])
        #    circuit.cx(qbr[idx_qb], qbr[idx_damp])
        #    circuit.ry(-theta[idx_qb]/2, qbr[idx_damp])
        #    circuit.cx(qbr[idx_qb], qbr[idx_damp])
        #    circuit.cx(qbr[idx_damp], qbr[idx_qb])

    stateop, result, _ = c2qa.util.simulate(circuit)
    density_matrix = DensityMatrix(np.asarray(c2qa.util.trace_out_qumodes(circuit, stateop)))
    rho_A.append(np.asarray(partial_trace(density_matrix,[1,2,3,4,5,6,7]))[1,1])
    rho_B.append(np.asarray(partial_trace(density_matrix,[0,2,3,4,5,6,7]))[1,1])
    rho_C.append(np.asarray(partial_trace(density_matrix,[0,1,3,4,5,6,7]))[1,1])

fig, ax = plt.subplots()
ax.set_title('Population Dynamics in the 1 state for Trotterized Hamiltonian')
ax.plot(time, rho_A)
ax.plot(time, rho_B)
ax.plot(time, rho_C)
ax.legend(['Transmon A', 'Transmon B', 'Transmon C'])

fig.savefig(output_name + '.png')

np.savetxt(output_name + '.out', (time, rho_A, rho_B, rho_C))
