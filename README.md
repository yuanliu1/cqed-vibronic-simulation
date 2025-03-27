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


## Contact <a name="contact"></a>

## License <a name="license"></a>
