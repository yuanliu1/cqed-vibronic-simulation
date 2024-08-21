import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

doubleplot = True # Whether to have the data be on separate graphs - expects a shadow datafile to compare both

datafile_A = 'data/standard/10000shots/amplitudedamping-3.15-9.45-3.15.out'
A_label = "Modified"

datafile_B = 'data/standard/10000shots/amplitudedamping-3.15-1.05-3.15.out'
B_label = "Lower"

shadow_datafile = 'data/standard/10000shots/amplitudedamping.out'
shadow_label = "Reference"

maincolorA = '#2f0033'
maincolorB = '#0500b4'
maincolorC = '#ff0000'
backgroundA = '#664169'
backgroundB = '#8686ff'
backgroundC = '#ff5b5b'


if doubleplot:
    fig, (ax1,ax2) = plt.subplots(2, 1)
    df = pd.read_csv(shadow_datafile, delimiter='\s*\(|[\+-]\d\.\d+e[\+-]\d+j\) *\(|[\+-]\d\.\d+e[\+-]\d+j\)', engine = 'python')
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
    df.columns = df.columns.map(float)
    data = df.to_numpy()
    columns = df.columns.to_numpy()
    ax1.plot(columns, data[0], '--', linewidth=1.5, label=shadow_label + " A", color=backgroundA)
    ax1.plot(columns, data[1], '--', linewidth=1.5, label=shadow_label + " B", color=backgroundB)
    ax1.plot(columns, data[2], '--', linewidth=1.5, label=shadow_label + " C", color=backgroundC)
    ax2.plot(columns, data[0], '--', linewidth=1.5, label=shadow_label + " A", color=backgroundA)
    ax2.plot(columns, data[1], '--', linewidth=1.5, label=shadow_label + " B", color=backgroundB)
    ax2.plot(columns, data[2], '--', linewidth=1.5, label=shadow_label + " C", color=backgroundC)
else:
    fig, axes = plt.subplots(1, 1)



df = pd.read_csv(datafile_A, delimiter='\s*\(|[\+-]\d\.\d+e[\+-]\d+j\) *\(|[\+-]\d\.\d+e[\+-]\d+j\)', engine = 'python')
df.drop(columns=df.columns[0], axis=1, inplace=True)
df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
df.columns = df.columns.map(float)
data = df.to_numpy()
columns = df.columns.to_numpy()
if doubleplot:
    ax1.plot(columns, data[0], linewidth=1.5, label=A_label + " A", color=maincolorA)
    ax1.plot(columns, data[1], linewidth=1.5, label=A_label + " B", color=maincolorB)
    ax1.plot(columns, data[2], linewidth=1.5, label=A_label + " C", color=maincolorC)
    ax1.legend(loc=0)
    ax1.set_yticks([0,.25,.5,.75,1],labels=['0.00',.25,'.50',.75,'1.00'],fontsize=12)
    ax1.set_xticks([0,.25,.5,.75,1,1.25,1.5,1.75,2],labels=['0.00',.25,'.50',.75,'1.00',1.25,'1.50',1.75,'2.00'],fontsize=12)
else:
    axes.plot(columns, data[0], '--', linewidth=1.5, label=A_label + " A", color=backgroundA)
    axes.plot(columns, data[1], '--', linewidth=1.5, label=A_label + " B", color=backgroundB)
    axes.plot(columns, data[2], '--', linewidth=1.5, label=A_label + " C", color=backgroundC)

df = pd.read_csv(datafile_B, delimiter='\s*\(|[\+-]\d\.\d+e[\+-]\d+j\) *\(|[\+-]\d\.\d+e[\+-]\d+j\)', engine = 'python')
df.drop(columns=df.columns[0], axis=1, inplace=True)
df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
df.columns = df.columns.map(float)
data = df.to_numpy()
columns = df.columns.to_numpy()
if doubleplot:
    ax2.plot(columns, data[0], linewidth=1.5, label=B_label + " A", color=maincolorA)
    ax2.plot(columns, data[1], linewidth=1.5, label=B_label + " B", color=maincolorB)
    ax2.plot(columns, data[2], linewidth=1.5, label=B_label + " C", color=maincolorC)
    #ax2.legend(loc=0)
    ax2.set_yticks([0,.25,.5,.75,1],labels=['0.00',.25,'.50',.75,'1.00'],fontsize=12)
    ax2.set_xticks([0,.25,.5,.75,1,1.25,1.5,1.75,2],labels=['0.00',.25,'.50',.75,'1.00',1.25,'1.50',1.75,'2.00'],fontsize=12)
else:
    axes.plot(columns, data[0], linewidth=1.5, label=B_label + " A", color=maincolorA)
    axes.plot(columns, data[1], linewidth=1.5, label=B_label + " B", color=maincolorB)
    axes.plot(columns, data[2], linewidth=1.5, label=B_label + " C", color=maincolorC)
    axes.legend(loc=0)
    axes.set_yticks([0,.2,.4,.6,.8,1],labels=[0.0,.2,.4,.6,.8,1.0],fontsize=12)
    axes.set_xticks([0,.25,.5,.75,1,1.25,1.5,1.75,2],labels=['0.00',.25,'.50',.75,'1.00',1.25,'1.50',1.75,'2.00'],fontsize=12)

# Creates a graph labeling system that works with a single graph or multiple graphs
fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel('Time (ps)', **{'size':14})
plt.ylabel('Average Population', labelpad=16, **{'size':14})

plt.show()