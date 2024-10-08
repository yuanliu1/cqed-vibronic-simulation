## Data
Here is all the data that we generated for our project. It is divided into three sections:

### /benchmarks
In the benchmarks folder we have our benchmark results for various fock levels, simulation shots, and trotter steps. We included the output for all of the runs, compiling them into seperate spreadsheets to observe the changes. All benchmarks were based on a default setting of 2^2 fock levels, 10000 shots, and 100 steps per picosecond, changing one variable at a time to see the effect it has on performance and simulation dynamics. Note that, since running these benchmarks, we were able to further optimize the code, reducing the required qubits by 4. As a result, the runtimes listed in this data may be higher than what we can expect from an actual simulation. However, the relative results, such as the relative increase in computational cost in cpu-time from an increase in fock levels from 2^2 to 2^3 should still be valid. We have also included a list of Hazel Cluster Hosts for reference - these can be cross-referenced with the output of the individual simulation runs to determine the system that performed the simulation. 

### /general
Here, we have the raw data for our project, most of which were used in our paper. We've included the png and raw data output, the latter of which can be used to generate new graphs.

### /paper_figures
In this folder we have the png and pdfs of the graphs that we used in our paper.
