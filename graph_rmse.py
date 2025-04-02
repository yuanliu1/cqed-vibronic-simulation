################################################################
##  Calculates the Root Mean Squared Error of a list of graphs
##    - compares all of the runs of a data element against itself (fully connected graph)
##    - and then compares the first data element agaisnt all of the others : 1-2, 1-3, 1-4, ... (fully connected bipartite graph)
################################################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

show_std_dev = True
normalize = True

## Folder locations and number of passes to compute the RSME of - expect quadratic growth in the number of comparisons
prefix = "data/benchmarks/sim_pass_"
passes_count = 5

### Benchmark Data - comment in/out whichever dataset to benchmark
## Fock level benchmarks
data = ["/amp_all3.15_dep_all0.9_Fock16_10k_10fs.out", "/amp_all3.15_dep_all0.9_Fock8_10k_10fs.out", "/amp_all3.15_dep_all0.9_Fock4_10k_10fs.out", "/amp_all3.15_dep_all0.9_Fock2_10k_10fs.out"]
## Trotter Step size benchmarks
#data = ["/amp_all3.15_dep_all0.9_Fock8_10k_5fs.out", "/amp_all3.15_dep_all0.9_Fock8_10k_10fs.out", "/amp_all3.15_dep_all0.9_Fock8_10k_20fs.out", "/amp_all3.15_dep_all0.9_Fock8_10k_40fs.out"]
## Shot count benchmarks
#data = ["/amp_all3.15_dep_all0.9_Fock8_20k_10fs.out","/amp_all3.15_dep_all0.9_Fock8_10k_10fs.out", "/amp_all3.15_dep_all0.9_Fock8_5k_10fs.out", "/amp_all3.15_dep_all0.9_Fock8_2500_10fs.out"]

datafiles = []
for file in data:
    sim_passes = []
    for x in range(passes_count):
        sim_passes.append(prefix + str(x+1) + file)
    datafiles.append(sim_passes)


def get_csv_data(file):
    ## The regex delimiter used to get the data from the C2QA output
    delimiter = '\s*\(|[\+-]\d\.\d+e[\+-]\d+j\) *\(|[\+-]\d\.\d+e[\+-]\d+j\)'
    ## Read in data
    df = pd.read_csv(file, delimiter=delimiter, engine = 'python')
    ## Drop first and last column, as they are blank (thanks to delimiter pattern used)
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
    df.columns = df.columns.map(float)
    rows = df.to_numpy()
    columns = df.columns.to_numpy()
    return rows, columns

## Assumes all datafiles are of the same trotter step size and duration
def get_data(datafiles):
    rows = []
    columns = []
    for x in range(len(datafiles)):
        row, column = get_csv_data(datafiles[x])
        rows.append(row)
        columns.append(column)
    #avg_rows = np.average(rows, axis=0)
    avg_chromophores = np.average(np.average(rows, axis=2), axis = 0)
    std_dev = np.std(rows, axis=0)
    avg_std_dev = np.average(std_dev, axis=1)
    return rows, columns[0], avg_std_dev, avg_chromophores


rowsA_list, columnsA, std_dev_A, avg_chromophores_A = get_data(datafiles[0])
std_devs = []
if normalize:
    std_dev_A = std_dev_A / avg_chromophores_A
std_devs.append(std_dev_A)

## compares the all of the runs of the first data element against each other
sum_squared = np.zeros(len(rowsA_list[0]))
n = np.zeros(len(rowsA_list[0]))

for i in range(0,len(datafiles[0])-1):
    for j in range(i,len(datafiles[0])):
        for x in range(len(rowsA_list[i])):
            for y in range(len(columnsA)):
                sum_squared[x] += np.square(rowsA_list[i][x][y] - rowsA_list[j][x][y])
                n[x] += 1

rmse = np.sqrt(sum_squared / n)
if normalize:
    rmse = rmse / avg_chromophores_A
print("1-1: " + str(rmse))

## compares the every run of the first data element against all of the runs of the other data elements
rowsB_list = []
columnsB = []
avg_chromophores_B = []
std_dev_B = 0
for i in range(1,len(datafiles)):
    rowsB_list, columnsB, std_dev_B, avg_chromophores_B = get_data(datafiles[i])
    if normalize:
        std_dev_B = std_dev_B / avg_chromophores_B
    std_devs.append(std_dev_B)
    #rmse = np.sqrt(np.square(rowsB - rowsA).mean())
    n = np.zeros(len(rowsA_list[0]))
    sum_squared = np.zeros(len(rowsA_list[0]))
    for j in range(len(rowsA_list)):
        for k in range(len(rowsB_list)):
            for x in range(len(rowsA_list[j])):
                y_b = 0
                for y in range(len(columnsA)):
                    while y_b < len(columnsB) and columnsA[y] >= columnsB[y_b]:
                        if columnsA[y] == columnsB[y_b]:
                            n[x] += 1
                            sum_squared[x] += np.square(rowsA_list[j][x][y] - rowsB_list[k][x][y_b])
                        y_b += 1
    rmse = 0
    rmse = np.sqrt(sum_squared / (n))
    if normalize:
        rmse = rmse / avg_chromophores_A
    print('1-' + str(i+1) + ': ' + str(rmse))
if show_std_dev:
    for x in range(len(std_devs)):
        print("std dev " + str(x+1) + ":" + str(std_devs[x]))
        


            
        
