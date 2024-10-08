# cQED Vibronic Simulation
## Description
This is a codebase for hardware-efficient ab initio quantum simulation of dissipative vibronic dynamics. Here, we have our simulation, graph creation, and parameter calculation code, as well as our data and figures that we were able to generate for our research paper. 

## Setup
We used a variety of software packages in our simulation, which are listed below, with the versions tested. Note that it is very likely that our code will work with other software versions, just that it was not tested. Note that the dependencies for c2qa are not listed, and should be referenced and installed based on instructions from **https://github.com/C2QA/bosonic-qiskit**. 

| Package | Version(s) |
|---------|------------|
| qutip | 5.0.1 |
| numpy | 1.23.2 |
| scipy | 1.9.1 |
| matplotlib | 3.5.3 |
| python | 3.10.11 |
| pandas | 1.4.4 |
| bosonic-qiskit | 11.2 ; 12.2.6 |

As bosonic-qiskit is not published to any package managers, the c2qa root folder needs to be added to the path before it can be imported. The simplest way of doing this is to have it in the same folder as the c2qa code that you are trying to run. Otherwise, the tutorials on their github show how it can be added to the path if the code and c2qa root folder are not in the same folder. 

![image](https://github.com/user-attachments/assets/4406eccd-5b7f-486b-a177-2ea22cfb5a68)

## Contents
Here is an explanation of all of the items in this repository
| Item | Description |
|---------|------------|
| /data/ | A repository of all the data and graphs generated for our paper |
| /3_chromophore_exact.ipynb | An exact simulation of our 3-chromophore system in qutip |
| /3_chromophore_vibronic_simulation.py | A statevector simulation of our 3-chromophore system using c2qa. |
| /benchmark_graphs.py | A specialized graph generator for diplaying multiple simulation runs against a single simulation run |
| /cd_fidelity.py | Calculates the possible ranges of conditional displacement error rates |
| /graph_creation.py | A general graph generator for displaying a n-length column of simulation graphs |
| /parameter_calculations.py | Calculates the various parameters for our simulation |
| /trajectorycombination.py | Combines multiple data files together, averaging their counts together. |
