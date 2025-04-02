# cQED Vibronic Simulation
## Description
This is a codebase for hardware-efficient ab initio quantum simulation of dissipative vibronic dynamics. Here, we have our simulation, graph creation, and parameter calculation code, as well as our data and figures that we were able to generate for our research paper. 

## Table of Contents

1. [Setup](#setup)
2. [Contents](#contents)
3. [Contact](#contact)
4. [License](#license)


## Setup <a name="setup"></a>
To set up the environment for executing the code in this repository, we recommend using a fresh `conda` environment to provide a cleaner python interface and avoid potential version conflicts. However, it is not necessary - all code should still run fine. The setup with or without conda should be the same. 

1. **Clone the Necessary Repositories** into the desired directory:
```
git clone https://github.com/yuanliu1/cqed-vibronic-simulation
git clone https://github.com/C2QA/bosonic-qiskit
```
2. **Switch to an older version of Bosonic Qiskit.** An older version is more likely to work (and necessary to work with our requirements.txt) with our code base. New changes may occur that have the potential to break certain aspects of existing code.
```
cd bosonic-qiskit
git checkout v12.2.6
cd ..
```
3. **Install Necessary Dependencies** using pip.
```
cd cqed-vibronic-simulation
pip install -r requirements.txt
```
4. **Add c2qa to path**

Move the `/bosonic-qiskit/c2qa` folder to `/cqed-vibronic-simulation/c2qa`. This can be done in whatever way is most convenient for your file system (be it dragging and dropping or a `mv` command). There are other ways to get python to load the module, but this is the simplest way. The file structure should look like this when you're done:

![image](https://github.com/user-attachments/assets/1e89b7b7-aabb-4718-8d04-03a06ef228f6)

## Contents <a name="contents"></a>
### Main Simulation (3_chromophore_vibronic_simulation.py)
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

where we have the output set to "test", with 400 steps at a 5fs step size, with 10000 shots and the default damping and dephasing channels. The output of this program will be two files in the current directory with names


## Contact <a name="contact"></a>

## License <a name="license"></a>
