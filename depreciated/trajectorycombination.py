import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

available_trajectories = 20

data_file_loc = 'data/undamped_tests/'
data_file_prefix = 'undamped-k_t-'
data_file_postfix = '.out'
data_file_start = 100
data_file_end = 100

data_files = []

data = []

for x in range(data_file_start, data_file_end + 1):
    data_files.append(data_file_loc + data_file_prefix + str(x) + data_file_postfix)

columns = []

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
    #print(columns[x][0])


mean = np.mean(data,axis=0)

plt.plot(columns[0], mean[0], label = 'Chromophore A')
plt.plot(columns[0], mean[1], label = 'Chromophore B')
plt.plot(columns[0], mean[2], label = 'Chromophore C')
plt.legend(loc='best')
plt.title('Population Dynamics in the Excited State')
plt.xlabel('Time (ps)')
plt.ylabel('Concentration')
plt.show()


