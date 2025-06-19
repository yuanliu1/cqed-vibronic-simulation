# cQED Vibronic Simulation
## Description
This is a codebase for hardware-efficient ab initio quantum simulation of dissipative vibronic dynamics. Here, we have our simulation, graph creation, and parameter calculation code, as well as our data and figures that we were able to generate for our research paper. 

## Table of Contents

1. [Setup](#setup)
2. [Contents](#contents)
   -  [Main Simulation](#main)
   -  [Supplementary Simulations](#supplementary)
      - [Exact Simulation](#exact)
      - [CNOT Noise](#cnotnoise)
      - [Conditional Displacement Noise](#cdnoise)
3. [Performance](#perf)
4. [Contact](#contact)
5. [License](#license)


## Setup <a name="setup"></a>
To set up the environment for executing the code in this repository, we recommend using a fresh `conda` environment to provide a cleaner python interface and avoid potential version conflicts. However, it is not necessary - all code should still run fine. The setup with or without conda should be the same. 

1. **Clone the Necessary Repositories** into the desired directory.
```
git clone https://github.com/yuanliu1/cqed-vibronic-simulation
cd cqed-vibronic-simulation
```
2. **Setup Python Environment.** This step is not strictly necessary, but highly recommended to maintain a clean working environment.
- With Anaconda
   - Setup : ```conda create -n NAME python=3.12```
      - NAME refers to the name of your conda environment. Note that the python version is necessary for the Jupyter Notebooks to function properly - it doesn't necessarily have to be Python 12.
   - Activation : ```conda activate NAME```
   - Deactivation: ```conda deactivate```
```
conda 
```
- Without Anaconda
   - Setup : ```python -m venv venv```
   - Activation : ```venv\Scripts\activate```
   - Deactivation: ```deactivate```
3. **Install Necessary Dependencies** using pip. Make sure to do this while the ```venv``` or ```conda``` environment is activated.
```
pip install -r requirements.txt
```

![image](https://github.com/user-attachments/assets/1e89b7b7-aabb-4718-8d04-03a06ef228f6)

## Contents <a name="contents"></a>
### Main Simulation (3_chromophore_vibronic_simulation.py) <a name="main"></a>
There are two ways to run our simulation: via the command line interface or through direct editing of the parameters in the code. The latter is relatively straightforwards - simply navigate to the "Simulation Parameters" section of the code and edit what is needed. As for the command line parameters, we require a total of 13 simulation parameters, a combination of integers (int), strings (str), and decimal values (flt) in the order below. Note that the environment must be set up before this code can run (see [Setup](#setup))

```
python ./3_chromophore_vibronic_simulation.py <output_name> <trotter_steps> <step_size> <shot_count> <qb_p_mode> <damp_toggle> <damp_a> <damp_b> <damp_c> <deph_toggle> <deph_a> <deph_b> <deph_c>

(str) output_name - name to give to output data - do not include file extension
(int) trotter_steps - number of iterations to run the simulation for
(flt) step_size - length of a single trotter step in picoseconds
(int) shot_count - number of shots to run in the simulator
(int) qb_p_mode - qubits per mode; each qubit doubles the available states in each mode.
(int) damp_toggle - toggle for amplitude damping channel. (0 = off, 1 = on)
(flt) damp_a - amplitude damping value for chromophore A (default = 3.15)
(flt) damp_b - amplitude damping value for chromophore B (default = 3.15)
(flt) damp_c - amplitude damping value for chromophore C (default = 3.15)
(int) deph_toggle - toggle for dephasing channel (0 = off, 1 = on)
(flt) deph_a - dephasing value for chromophore A (default = 0.9)
(flt) deph_b - dephasing value for chromophore B (default = 0.9)
(flt) deph_c - dephasing value for chromophore C (default = 0.9)
```

An example of a proper command is provided below,

```
python ./3_chromophore_vibronic_simulation.py test 400 0.005 10000 3 1 3.15 3.15 3.15 1 0.9 0.9 0.9
```

where we have the output set to "test", with 400 steps at a 5fs step size, with 10000 shots and the default damping and dephasing channels turned on. 

The output of this program will be two files in the directory from which the code is executed with names "<output_name>.out", containing raw data, and "<output_name>.png", containing a graph of the data. The filetype of the graphical representation can be changed if desired by changing the ```output_filetype``` parameter in the code to anything that is supported by matplotlib's pyplot (e.g. "pdf", "svg") while the ".out" files can all be used for further data processing and aggregation.

### Supplementary Simulations <a name="supplementary"></a>

**3_chromophore_exact.py** <a name="exact"></a>

This is an exact simulation of the 3-chromophore system that we are modeling in QuTiP, which graphs the output of the exact simulation against a specified data file. We were unable to simulate with the amplitude damping and dephasing channels so the output can only be compared against another noiseless simulation. There are no command line parameters to be specified as this code is relatively inflexible due to it's singular purpose of providing a comparison point to ensure that our Trotter simulation was correct. 

**3_chromophore_vibornic_simulation_cnot_noise.ipynb** <a name="cnotnoise"></a>

This Jupyter notebook adds varying levels of CNOT noise using the qiskit noise model to our simulation, to see what are acceptable noise parameters for our simulation, if we were to simulate on a real system. You can execute this the same way as any other Jupyter notebook.

**3_chromophore_vibornic_simulation_CD_noise.ipynb** <a name="cdnoise"></a>

This Jupyter notebook tests to see what effect realistic Conditional Displacement infidelity rates will have on our simulation. You can execute this the same way as any other Jupyter notebook.


## Performance <a name="perf"></a>

In terms of runtime, these simulations may take a long time to run, depending on the parameters chosen. As expected, changes in trotter step and shot counts provide a linear time scaling (a 2x increase in either count will result in a 2x increase in runtime). It gets more interesting with the enabling of noise channels and varying fock levels. The elimination of noise channels or a reduction in qubits per qumode provide exponential decreases in runtime, thanks to the limitations of classical simulation. Additionally, the choice of simulation hardware also matters - GPUs can provide a considerable speedup in simulation time if they are available. However, as of right now, Bosonic Qiskit does not directly support GPU simulation - it'll be necessary to modify the c2qa source code to enable it. If you are interested in GPU simulation, contact us and we can assist. Otherwise, old but relevant CPU runtime data can be located in this repository under ```data/benchmarks/runtimes.xlsx``` - these numbers can be easily extrapolated to fit your current system. 

## Contact <a name="contact"></a>

For questions, comments, or support, contact:

Daniel Dong (ddong2@ncsu.edu, danieldong1.618@gmail.com)

Nam Vu (vu_p_nam@mit.edu)

## License <a name="license"></a>
