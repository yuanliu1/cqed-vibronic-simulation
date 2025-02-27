################################################################
##  As the C2QA package is not currently published to any package managers, 
##  to use the package, add the 'c2qa' folder to the same folder as this code
################################################################
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
import numpy as np
import matplotlib.pyplot as plt
from qiskit import ClassicalRegister, QuantumRegister
from qiskit_aer.library import SaveDensityMatrix

################################################################
##  Simulation Parameters
################################################################

## Name of output files- use sys.argv[1] if you want to set output name via command line
output_name = sys.argv[9]  # There will be a *.out and a *.{filetype} file if the simulation is successful
output_filetype = "png" # The filetype for the matplotlib output - recommendations: 'png' or 'pdf'

## Circuit parameters
global numberofmodes, numberofqubitspermode
numberofmodes=4         # Number of qumodes in the simulation
numberofqubitspermode=sys.argv[8] # Number of qubits for each qumode. Fock level = 2^(#qubits).

## Simulation parameters
sim_steps = int(sys.argv[1])          # The number of steps in the trotter simulation
timestep = float(sys.argv[2])         # The timestep for the trotter simulation
shots = int(sys.argv[3])              # Number of shots to run the simulation for - necessary only for damping channels
amplitude_damping = False # Toggles on or off the amplitude damping channel
dephasing = False         # Toggles on or off the dephasing channel
time = np.round(np.arange(sim_steps) * timestep, 5)

## Damping rates; damping probability = sin(theta/2)^2 = (gamma_all*timestep)
## Amplitude Damping Rate and conversion to theta
gamma_damp = np.array([3.15e12/1e12, float(sys.argv[4]), 3.15e12/1e12]) # [gamma_a, gamma_b, gamma_c, gamma_l]
theta_damp = 2*np.arcsin(np.sqrt(gamma_damp*timestep))
## Dephasing Rate and conversion to theta
gamma_dephase = np.array([9.0e11/1e12, float(sys.argv[5]), 9.0e11/1e12]) # [gamma_a, gamma_b, gamma_c, gamma_l]
theta_dephase = 2*np.arcsin(np.sqrt(gamma_dephase*timestep))

if int(sys.argv[6]) == 1:
    amplitude_damping = True
if int(sys.argv[7]) == 1:
    dephasing = True

## Global parameters
omega = np.array([4.79e13, 4.8e13, 4.785e13, 6e12])/1e12 # omega_a,b,c,l
delta_qa = np.array([5.00400599e11, 4.99487607e10])/1e12            # delta_ab,ac
chi = np.array([-3.2e12, -3.6e12, -2.7e12])/1e12         # chi_a,b,c
g_cd = np.array([3.38326237e12, 3.03151748e12, 3.70349480e12])/1e12    # g_cda,cdb,cdc
g_cdl = (1.341640786499e12+0.0j)/1e12                            # g_cdl
g_a = np.array([3e12, 2.7e12])/1e12                      # g_ab,ac
g_al = np.array([-3e11, 4.05e11])/1e12                   # g_abl,acl

################################################################
##  Circuit Building
################################################################

## Test Circuit to ensure that c2qa works
qmr_test = c2qa.QumodeRegister(4, num_qubits_per_qumode = 2)
circuit_test = c2qa.CVCircuit(qmr_test)

circuit_test.cv_r(-4.79e12,qmr_test[0])
circuit_test.cv_r(-4.8e12,qmr_test[1])
circuit_test.cv_r(-4.79e12,qmr_test[2])
circuit_test.cv_r(-6e11,qmr_test[3])

_, result, _ = c2qa.util.simulate(circuit_test)

## Build circuit for exp(-iH_0*tau) Needs trotterization.
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
    
## Build circuit for exp(-iH_1*tau)
def H1(tau, chi_list = chi, g_cd_list = g_cd, reverse = False):
    chi_t = tau*chi_list/(2)
    g_cdt = tau*g_cd_list/(2)*1j*(-1)
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

##title Build circuit for $\exp{(-iH_2\tau)}$ Rotated version: Split H2XX and H2YY
def H2XX(tau, g_cdl=g_cdl, g_a_list=g_a, g_al_list=g_al, reverse = False):
    g_at = 2*tau*g_a_list
    g_alt = -1j*tau*g_al_list
    if not reverse:
        for i_qumode in range(2): # ab and ac
            circuit.rxx(g_at[i_qumode]/2, qbr[0], qbr[1+i_qumode])

        # Displaced qb for l controlled by sigma_a^x
        circuit.swap(qbr[0], anc[0])
        circuit.cv_c_d(-1j*g_cdl*tau/(4), qmr[3], anc[0])
        circuit.swap(qbr[0], anc[0])
        circuit.barrier()

        # Displaced qb for l controlle by sigma_a^x*sigma_(b or c)^x
        for i_qumode in range(1,3):
            circuit.h(qbr[0])
            circuit.h(qbr[i_qumode])
            circuit.cx(qbr[i_qumode], qbr[0])
            circuit.swap(qbr[0], anc[0])
            circuit.cv_c_d(g_alt[i_qumode-1]/2, qmr[3], anc[0])
            circuit.swap(qbr[0], anc[0])
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
            circuit.swap(qbr[0], anc[0])
            circuit.cv_c_d(g_alt[-i_qumode]/2, qmr[3], anc[0])
            circuit.swap(qbr[0], anc[0])
            circuit.cx(qbr[r_i_qumode], qbr[0])
            circuit.h(qbr[0])
            circuit.h(qbr[r_i_qumode])
            circuit.barrier()

        # Displaced qb for l controlled by sigma_a^x
        circuit.swap(qbr[0], anc[0])
        circuit.cv_c_d(-1j*g_cdl*tau/(4), qmr[3], anc[0])
        circuit.swap(qbr[0], anc[0])
        circuit.barrier()

        for i_qumode in range(2): # ab and ac
            r_i_qumode = 1-i_qumode # reverse index
            circuit.rxx(g_at[-i_qumode-1]/2, qbr[0], qbr[1+r_i_qumode])

def H2YY(tau, g_cdl=g_cdl, g_a_list=g_a, g_al_list=g_al, reverse = False):
    g_at = 2*tau*g_a_list
    g_alt = -1j*tau*g_al_list
    if not reverse:
        for i_qumode in range(2): # ab and ac
            circuit.ryy(g_at[i_qumode]/2, qbr[0], qbr[1+i_qumode])

        # Displaced qb for l controlled by sigma_a^x
        circuit.swap(qbr[0], anc[0])
        circuit.cv_c_d(-1j*g_cdl*tau/(4), qmr[3], anc[0])
        circuit.swap(qbr[0], anc[0])
        circuit.barrier()

        # Displaced qb for l controlled by sigma_a^x*sigma_(b or c)^x
        for i_qumode in range(1,3):
            circuit.rz(-np.pi/2,qbr[0])
            circuit.h(qbr[0])
            circuit.rz(-np.pi/2,qbr[i_qumode])
            circuit.h(qbr[i_qumode])
            circuit.cx(qbr[i_qumode], qbr[0])
            circuit.swap(qbr[0], anc[0])
            circuit.cv_c_d(g_alt[i_qumode-1]/2, qmr[3], anc[0])
            circuit.swap(qbr[0], anc[0])
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
            circuit.swap(qbr[0], anc[0])
            circuit.cv_c_d(g_alt[-i_qumode]/2, qmr[3], anc[0])
            circuit.swap(qbr[0], anc[0])
            circuit.cx(qbr[r_i_qumode], qbr[0])
            circuit.h(qbr[0])
            circuit.rz(-np.pi/2,qbr[0])
            circuit.h(qbr[r_i_qumode])
            circuit.rz(-np.pi/2,qbr[r_i_qumode])
            circuit.barrier()

        # Displaced qb for l controlled by sigma_a^x
        circuit.swap(qbr[0], anc[0])
        circuit.cv_c_d(-1j*g_cdl*tau/(4), qmr[3], anc[0])
        circuit.swap(qbr[0], anc[0])
        circuit.barrier()

        for i_qumode in range(2): # ab and ac
            r_i_qumode = 1-i_qumode # reverse index
            circuit.ryy(g_at[-i_qumode-1]/2, qbr[0], qbr[1+r_i_qumode])

################################################################
##  Circuit Simulation
################################################################

## Data arrays
rho_A = []
rho_B = []
rho_C = []

## Circuit initialization
qmr = c2qa.QumodeRegister(num_qumodes=numberofmodes, num_qubits_per_qumode=numberofqubitspermode)
qbr = QuantumRegister(size = numberofmodes-1)
anc = QuantumRegister(size = 1)
cbits = ClassicalRegister(size = numberofmodes)
circuit = c2qa.CVCircuit(qmr, qbr, anc, cbits)
circuit.x(qbr[0])

## Build trotter simulation
for i in range(sim_steps):
    if i != 0:
        H0(timestep/2)
        H1(timestep/2)
        H2XX(timestep/2)
        H2YY(timestep/2)
        H2YY(timestep/2, reverse = True)
        H2XX(timestep/2, reverse = True)
        H1(timestep/2, reverse = True)
        H0(timestep/2, reverse = True)
        # Amplitude damping channel inspired by https://arxiv.org/pdf/2302.14592.pdf (Fig 8)
        idx_damp = 3
        if (amplitude_damping):
            for idx_qb in range(numberofmodes - 1):
                circuit.cry(theta_damp[idx_qb], qbr[idx_qb], anc[0])
                circuit.cx(anc[0], qbr[idx_qb])
                circuit.measure(anc[0], cbits[idx_damp])
                circuit.reset(anc[0])
        # Dephasing Channel
        if (dephasing):
            for idx_qb in range(numberofmodes - 1):
                circuit.ry(theta_dephase[idx_qb], anc[0])
                circuit.cz(qbr[idx_qb], anc[0])
                circuit.measure(anc[0], cbits[idx_damp])
                circuit.reset(anc[0])

    # We are able dramatically improve run times by saving the density matrix after every trotter step
    save_densitymatrix = SaveDensityMatrix(1, label='densitymatrix_a{}'.format(i))
    circuit.append(save_densitymatrix, [qbr[0]])
    save_densitymatrix = SaveDensityMatrix(1, label='densitymatrix_b{}'.format(i))
    circuit.append(save_densitymatrix, [qbr[1]])
    save_densitymatrix = SaveDensityMatrix(1, label='densitymatrix_c{}'.format(i))
    circuit.append(save_densitymatrix, [qbr[2]])
    
## Simulate Circuit and obtain output data
stateop, result, _ = c2qa.util.simulate(circuit, shots=shots)
data = result.data()

## Extract saved Density Matrix data
for i in range(sim_steps):
    rho_A.append(np.asarray(data['densitymatrix_a{}'.format(i)])[1,1])
    rho_B.append(np.asarray(data['densitymatrix_b{}'.format(i)])[1,1])
    rho_C.append(np.asarray(data['densitymatrix_c{}'.format(i)])[1,1])

## Graphing population dynamics
fig, ax = plt.subplots()
ax.set_title('Population Dynamics in the 1 state for Trotterized Hamiltonian')
ax.plot(time, rho_A, '#2F0033')
ax.plot(time, rho_B, '#0500B4')
ax.plot(time, rho_C, '#FF0000')
ax.legend(['Transmon A', 'Transmon B', 'Transmon C'])

## Saving Graph and output file
fig.savefig(output_name + '.' + output_filetype)
np.savetxt(output_name + '.out', (time, rho_A, rho_B, rho_C))
