import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

doubleplot = False
shadowplot = False

if doubleplot:
    fig, (ax1,ax2) = plt.subplots(2, 1)
    if shadowplot:
        data_file = 'data/final/10000shots_updated/lowerphasedamping.out'
        df = pd.read_csv(data_file, delimiter='\s*\(|[\+-]\d\.\d+e[\+-]\d+j\) *\(|[\+-]\d\.\d+e[\+-]\d+j\)', engine = 'python')
        df.drop(columns=df.columns[0], axis=1, inplace=True)
        df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
        df.columns = df.columns.map(float)
        data = df.to_numpy()
        columns = df.columns.to_numpy()
        ax1.plot(columns, data[0], '--', linewidth=1.5, label="Undamped A", color='#664169')
        ax1.plot(columns, data[1], '--', linewidth=1.5, label="Undamped B", color='#8686ff')
        ax1.plot(columns, data[2], '--', linewidth=1.5, label="Undamped C", color='#ff5b5b')
        ax2.plot(columns, data[0], '--', linewidth=1.5, label="Undamped A", color='#664169')
        ax2.plot(columns, data[1], '--', linewidth=1.5, label="Undamped B", color='#8686ff')
        ax2.plot(columns, data[2], '--', linewidth=1.5, label="Undamped C", color='#ff5b5b')
else:
    fig, axes = plt.subplots(1, 1)



data_file = 'data/final/10000shots_updated/nodamping.out'
df = pd.read_csv(data_file, delimiter='\s*\(|[\+-]\d\.\d+e[\+-]\d+j\) *\(|[\+-]\d\.\d+e[\+-]\d+j\)', engine = 'python')
df.drop(columns=df.columns[0], axis=1, inplace=True)
df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
df.columns = df.columns.map(float)
data = df.to_numpy()
columns = df.columns.to_numpy()
if doubleplot:
    ax1.plot(columns, data[0], linewidth=1.5, label="Undamped A", color='#2f0033')
    ax1.plot(columns, data[1], linewidth=1.5, label="Undamped B", color='#0500b4')
    ax1.plot(columns, data[2], linewidth=1.5, label="Undamped C", color='#ff0000')
    ax1.legend(loc=0)
    ax1.set_yticks([0,.25,.5,.75,1],labels=['0.00',.25,'.50',.75,'1.00'],fontsize=12)
    ax1.set_xticks([0,.25,.5,.75,1,1.25,1.5,1.75,2],labels=['0.00',.25,'.50',.75,'1.00',1.25,'1.50',1.75,'2.00'],fontsize=12)
else:
    axes.plot(columns, data[0], '--', linewidth=1.5, label="100 steps", color='#664169')
    axes.plot(columns, data[1], '--', linewidth=1.5, label="100 steps", color='#8686ff')
    axes.plot(columns, data[2], '--', linewidth=1.5, label="100 steps", color='#ff5b5b')

data_file = 'data/final/10000shots_updated/lowerphasedamping.out'
df = pd.read_csv(data_file, delimiter='\s*\(|[\+-]\d\.\d+e[\+-]\d+j\) *\(|[\+-]\d\.\d+e[\+-]\d+j\)', engine = 'python')
df.drop(columns=df.columns[0], axis=1, inplace=True)
df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
df.columns = df.columns.map(float)
data = df.to_numpy()
columns = df.columns.to_numpy()
if doubleplot:
    ax2.plot(columns, data[0], linewidth=1.5, label="Dephased A", color='#2f0033')
    ax2.plot(columns, data[1], linewidth=1.5, label="Dephased B", color='#0500b4')
    ax2.plot(columns, data[2], linewidth=1.5, label="Dephased C", color='#ff0000')
    #ax2.legend(loc=0)
    ax2.set_yticks([0,.25,.5,.75,1],labels=['0.00',.25,'.50',.75,'1.00'],fontsize=12)
    ax2.set_xticks([0,.25,.5,.75,1,1.25,1.5,1.75,2],labels=['0.00',.25,'.50',.75,'1.00',1.25,'1.50',1.75,'2.00'],fontsize=12)
else:
    axes.plot(columns, data[0], linewidth=1.5, label="Damped A", color='#2f0033')
    axes.plot(columns, data[1], linewidth=1.5, label="Damped B", color='#0500b4')
    axes.plot(columns, data[2], linewidth=1.5, label="Damped C", color='#ff0000')
    axes.legend(loc=0)
    axes.set_yticks([0,.2,.4,.6,.8,1],labels=[0.0,.2,.4,.6,.8,1.0],fontsize=12)
    axes.set_xticks([0,.25,.5,.75,1,1.25,1.5,1.75,2],labels=['0.00',.25,'.50',.75,'1.00',1.25,'1.50',1.75,'2.00'],fontsize=12)

fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel('Time (ps)', **{'size':14})
plt.ylabel('Average Population', labelpad=16, **{'size':14})

plt.show()