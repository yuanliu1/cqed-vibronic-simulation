################################################################
##  Calculates the Root Mean Squared Error of a list of graphs, in the order,
##  1-2, 2-3, 3-4, ... if (mode = 0) and
##  1-2, 1-3, 1-4, ... if (mode != 0)
################################################################

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

mode = 0
show_std_dev = False
normalize = True

#datafiles = [["data/benchmarks/fock_level/data/32fock_1.out", "data/benchmarks/fock_level/data/32fock_2.out", "data/benchmarks/fock_level/data/32fock_3.out"],
#             ["data/benchmarks/fock_level/data/16fock_1.out", "data/benchmarks/fock_level/data/16fock_2.out", "data/benchmarks/fock_level/data/16fock_3.out"],
#             ["data/benchmarks/fock_level/data/8fock_1.out", "data/benchmarks/fock_level/data/8fock_2.out", "data/benchmarks/fock_level/data/8fock_3.out"],
#             ["data/benchmarks/fock_level/data/4fock_1.out", "data/benchmarks/fock_level/data/4fock_2.out","data/benchmarks/fock_level/data/4fock_3.out"],
#             ["data/benchmarks/fock_level/data/2fock_1.out", "data/benchmarks/fock_level/data/2fock_2.out", "data/benchmarks/fock_level/data/2fock_3.out"]]
#datafiles = [["data/benchmarks/fock_level/data/noisy-8fock_1.out", "data/benchmarks/fock_level/data/noisy-8fock_2.out", "data/benchmarks/fock_level/data/noisy-8fock_3.out"],
#             ["data/benchmarks/fock_level/data/noisy-4fock_1.out", "data/benchmarks/fock_level/data/noisy-4fock_2.out","data/benchmarks/fock_level/data/noisy-4fock_3.out"],
#             ["data/benchmarks/fock_level/data/noisy-2fock_1.out", "data/benchmarks/fock_level/data/noisy-2fock_2.out", "data/benchmarks/fock_level/data/noisy-2fock_3.out"]]
#datafiles = [["data/benchmarks/trotter/data/5fs_1.out", "data/benchmarks/trotter/data/5fs_2.out", "data/benchmarks/trotter/data/5fs_3.out"],
#            ["data/benchmarks/trotter/data/10fs_1.out", "data/benchmarks/trotter/data/10fs_2.out", "data/benchmarks/trotter/data/10fs_3.out"], 
#            ["data/benchmarks/trotter/data/20fs_1.out", "data/benchmarks/trotter/data/20fs_2.out", "data/benchmarks/trotter/data/20fs_3.out"],
#             ["data/benchmarks/trotter/data/40fs_1.out", "data/benchmarks/trotter/data/40fs_2.out", "data/benchmarks/trotter/data/40fs_3.out"]]
#datafiles = [["data/benchmarks/shots/data/20000shots_1.out", "data/benchmarks/shots/data/20000shots_2.out", "data/benchmarks/shots/data/20000shots_3.out"],
#            ["data/benchmarks/shots/data/10000shots_1.out", "data/benchmarks/shots/data/10000shots_2.out", "data/benchmarks/shots/data/10000shots_3.out"],
#             ["data/benchmarks/shots/data/5000shots_1.out", "data/benchmarks/shots/data/5000shots_2.out", "data/benchmarks/shots/data/5000shots_3.out"],
#             ["data/benchmarks/shots/data/2500shots_1.out", "data/benchmarks/shots/data/2500shots_2.out", "data/benchmarks/shots/data/2500shots_3.out"]]
#datafiles = [["data/benchmarks/trotter/data/5fs_1.out"], ["data/benchmarks/trotter/data/5fs_2.out"], ["data/benchmarks/trotter/data/5fs_3.out"], ["data/benchmarks/trotter/data/5fs_1.out"]] # Use mode 0
#datafiles = [["data/benchmarks/shots/data/20000shots_1.out"], ["data/benchmarks/shots/data/20000shots_2.out"], ["data/benchmarks/shots/data/20000shots_3.out"], ["data/benchmarks/shots/data/20000shots_1.out"]] # Use mode 0
datafiles = [["data/benchmarks/fock_level/data/32fock_1.out"], ["data/benchmarks/fock_level/data/32fock_2.out"], ["data/benchmarks/fock_level/data/32fock_3.out"], ["data/benchmarks/fock_level/data/32fock_1.out"]]

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


rowsA_list, columnsA, std_dev_A, avg_chromophores_A= get_data(datafiles[0])
std_devs = []
if normalize:
    std_dev_A = std_dev_A / avg_chromophores_A
std_devs.append(std_dev_A)
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

    if mode == 0:
        rowsA_list = rowsB_list
        columnsA = columnsB
        print(str(i) + '-' + str(i+1) + ": " + str(rmse))
    else:
        print('1-' + str(i+1) + ': ' + str(rmse))
if show_std_dev:
    for x in range(len(std_devs)):
        print("std dev " + str(x+1) + ":" + str(std_devs[x]))
    


