import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

mode = 0 # 0 means fock level benchmark, 1 means trotter benchmark

if mode == 0:
    secondarydata = ['data/benchmarks/fock_level/data/reducedancillas_16fock_1.out', 'data/benchmarks/fock_level/data/reducedancillas_16fock_2.out', 'data/benchmarks/fock_level/data/reducedancillas_16fock_3.out']
    datafile = 'data/benchmarks/fock_level/data/benchmark_reducedancillas_2fock.out'
    s_label = "16-level"
    d_label = "2-level"
else:
    secondarydata = ['data/benchmarks/trotter/data/benchmark_reducedancillas_800step_1.out', 'data/benchmarks/trotter/data/benchmark_reducedancillas_800step_2.out', 'data/benchmarks/trotter/data/benchmark_reducedancillas_800step_3.out']
    datafile = 'data/benchmarks/trotter/data/benchmark_reducedancillas_200step_1.out'
    s_label = "10 fs step"
    d_label = "2.5 fs step"

maincolorA = '#2f0033'
maincolorB = '#0500b4'
maincolorC = '#ff0000'
secondarycolorA = '#664169'
secondarycolorB = '#8686ff'
secondarycolorC = '#ff5b5b'

fig, axes = plt.subplots(1, 1)



df = pd.read_csv(datafile, delimiter='\s*\(|[\+-]\d\.\d+e[\+-]\d+j\) *\(|[\+-]\d\.\d+e[\+-]\d+j\)', engine = 'python')
df.drop(columns=df.columns[0], axis=1, inplace=True)
df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
df.columns = df.columns.map(float)
data = df.to_numpy()
columns = df.columns.to_numpy()
axes.plot(columns, data[0], linewidth=1.5, label=d_label + " A", color=maincolorA, zorder=2.5)
axes.plot(columns, data[1], linewidth=1.5, label=d_label + " B", color=maincolorB, zorder=2.5)
axes.plot(columns, data[2], linewidth=1.5, label=d_label + " C", color=maincolorC, zorder=2.5)

nolegend = True #Ensures only one legend is printed for secondary data
for file in secondarydata:
    df = pd.read_csv(file, delimiter='\s*\(|[\+-]\d\.\d+e[\+-]\d+j\) *\(|[\+-]\d\.\d+e[\+-]\d+j\)', engine = 'python')
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
    df.columns = df.columns.map(float)
    data = df.to_numpy()
    columns = df.columns.to_numpy()
    axes.plot(columns, data[0], '--', linewidth=1.5, color=secondarycolorA)
    axes.plot(columns, data[1], '--', linewidth=1.5, color=secondarycolorB)
    axes.plot(columns, data[2], '--', linewidth=1.5, color=secondarycolorC)
    if nolegend:
        axes.plot(columns, data[0], '--', linewidth=1.5, label=s_label + " A", color=secondarycolorA)
        axes.plot(columns, data[1], '--', linewidth=1.5, label=s_label + " B", color=secondarycolorB)
        axes.plot(columns, data[2], '--', linewidth=1.5, label=s_label + " C", color=secondarycolorC)
        nolegend = False

fig.add_subplot(111, frameon=False)

axes.legend(loc=0)
axes.set_yticks([0,.2,.4,.6,.8,1],labels=[0.0,.2,.4,.6,.8,1.0],fontsize=12)
axes.set_xticks([0,.25,.5,.75,1,1.25,1.5,1.75,2],labels=['0.00',.25,'0.50',.75,'1.00',1.25,'1.50',1.75,'2.00'],fontsize=12)
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel('Time (ps)', **{'size':14})
plt.ylabel('Average Population', labelpad=7, **{'size':14})
plt.show()