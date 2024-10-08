import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

#########################################################
##  Code to combine a series of data files into one. 
##  
##  This can be useful for longer simulations, to split up the work 
##  between multiple compute nodes. We were able to optimize the code
##  the point where is code is redundant for our system size of 3 chromophores
#########################################################

## Series of data files to combine
data_file_loc = 'data/undamped_tests/'
data_file_prefix = 'undamped-k_t-'
data_file_postfix = '.out'
data_file_start = 1
data_file_end = 10

## Create a list of data files
data_files = []
for x in range(data_file_start, data_file_end + 1):
    data_files.append(data_file_loc + data_file_prefix + str(x) + data_file_postfix)

## Data
columns = []
data = []

## Collecting Data
for x in range(len(data_files)):
    # print(data_files[x])
    df = pd.read_csv(data_files[x], delimiter='\s*\(|[\+-]\d\.\d+e[\+-]\d+j\) *\(|[\+-]\d\.\d+e[\+-]\d+j\)', engine = 'python')
    ## Drop first and last column, as they are blank (thanks to delimiter pattern used)
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
    df.columns = df.columns.map(float)
    # print(df)
    data.append(df.to_numpy())
    columns.append(df.columns.to_numpy())
    # print(columns[x][0])

## Data aggregation
mean = np.mean(data,axis=0)

## Plotting data
plt.plot(columns[0], mean[0], label = 'Chromophore A')
plt.plot(columns[0], mean[1], label = 'Chromophore B')
plt.plot(columns[0], mean[2], label = 'Chromophore C')
plt.legend(loc='best')
plt.title('Population Dynamics in the Excited State')
plt.xlabel('Time (ps)')
plt.ylabel('Concentration')
plt.show()


