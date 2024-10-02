import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

################################################################
## Tripleplot paradigm will be: (main ; background)
#  Top graph - datafile_A ; background_A
#  Middle graph - datafile_B ; background_B
#  Bottom graph - datafile_C ; background_C
## Singleplot paradigm will be: (main ; background)
#  datafile_A ; background_A
################################################################

tripleplot = False # Whether to have the data be on separate graphs
comparison = True # Whether to have the comparison background graph behind every graph
enable_legend = True # Whether to enable the graph legend
axis_loc = 1
data_zorder = 2.5

datafile_A = 'data/general/bothdamping.out'
A_label = "Damped & Dephased"

datafile_B = 'data/general/phasedamping-0.9-2.7-0.9.out'
B_label = "Incr."

datafile_C = 'data/general/phasedamping-0.9-0.3-0.9.out'
C_label = "Decr."

background_A = 'data/general/amplitudedamping.out'
background_A_label = "Damped"

background_B = datafile_A
background_B_label = A_label

background_C = datafile_A
background_C_label = A_label

# Leave blank for no markers - see https://matplotlib.org/stable/api/markers_api.html
secondary_marker = ''

maincolorA = '#2f0033'
maincolorB = '#0500b4'
maincolorC = '#ff0000'
secondaryA = '#664169'
secondaryB = '#8686ff'
secondaryC = '#ff5b5b'

y_pad = 7

# The regex delimiter used to get the data from the C2QA output
delimiter = '\s*\(|[\+-]\d\.\d+e[\+-]\d+j\) *\(|[\+-]\d\.\d+e[\+-]\d+j\)'

if tripleplot:
    fig = plt.figure()
    gs = fig.add_gridspec(3, hspace=0)
    (ax1,ax2,ax3) = gs.subplots(sharex=True, sharey=True)
    
else:
    fig, ax1 = plt.subplots(1, 1)


df = pd.read_csv(datafile_A, delimiter=delimiter, engine = 'python')
df.drop(columns=df.columns[0], axis=1, inplace=True)
df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
df.columns = df.columns.map(float)
data = df.to_numpy()
columns = df.columns.to_numpy()
ax1.plot(columns, data[0], linewidth=1.5, label=A_label + " A", color=maincolorA, zorder=data_zorder)
ax1.plot(columns, data[1], linewidth=1.5, label=A_label + " B", color=maincolorB, zorder=data_zorder)
ax1.plot(columns, data[2], linewidth=1.5, label=A_label + " C", color=maincolorC, zorder=data_zorder)

if comparison:
    df = pd.read_csv(background_A, delimiter=delimiter, engine = 'python')
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
    df.columns = df.columns.map(float)
    data = df.to_numpy()
    columns = df.columns.to_numpy()
    ax1.plot(columns, data[0], '--', linewidth=1.5, label=background_A_label + " A", color=secondaryA, marker=secondary_marker)
    ax1.plot(columns, data[1], '--', linewidth=1.5, label=background_A_label + " B", color=secondaryB, marker=secondary_marker)
    ax1.plot(columns, data[2], '--', linewidth=1.5, label=background_A_label + " C", color=secondaryC, marker=secondary_marker)

if enable_legend:
    ax1.legend(loc=axis_loc)
ax1.set_yticks([0,.2,.4,.6,.8,1],labels=[0.0,.2,.4,.6,.8,1.0],fontsize=12)
ax1.set_xticks([0,.25,.5,.75,1,1.25,1.5,1.75,2],labels=['0.00',.25,'0.50',.75,'1.00',1.25,'1.50',1.75,'2.00'],fontsize=12)


if tripleplot:
    df = pd.read_csv(datafile_B, delimiter=delimiter, engine = 'python')
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
    df.columns = df.columns.map(float)
    data = df.to_numpy()
    columns = df.columns.to_numpy()
    ax2.plot(columns, data[0], linewidth=1.5, label=B_label + " A", color=maincolorA, zorder=data_zorder)
    ax2.plot(columns, data[1], linewidth=1.5, label=B_label + " B", color=maincolorB, zorder=data_zorder)
    ax2.plot(columns, data[2], linewidth=1.5, label=B_label + " C", color=maincolorC, zorder=data_zorder)

    df = pd.read_csv(datafile_C, delimiter=delimiter, engine = 'python')
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
    df.columns = df.columns.map(float)
    data = df.to_numpy()
    columns = df.columns.to_numpy()
    ax3.plot(columns, data[0], linewidth=1.5, label=C_label + " A", color=maincolorA, zorder=data_zorder)
    ax3.plot(columns, data[1], linewidth=1.5, label=C_label + " B", color=maincolorB, zorder=data_zorder)
    ax3.plot(columns, data[2], linewidth=1.5, label=C_label + " C", color=maincolorC, zorder=data_zorder)

    if comparison:
        df = pd.read_csv(background_B, delimiter=delimiter, engine = 'python')
        df.drop(columns=df.columns[0], axis=1, inplace=True)
        df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
        df.columns = df.columns.map(float)
        data = df.to_numpy()
        columns = df.columns.to_numpy()
        ax2.plot(columns, data[0], '--', linewidth=1.5, label=background_B_label + " A", color=secondaryA, marker=secondary_marker)
        ax2.plot(columns, data[1], '--', linewidth=1.5, label=background_B_label + " B", color=secondaryB, marker=secondary_marker)
        ax2.plot(columns, data[2], '--', linewidth=1.5, label=background_B_label + " C", color=secondaryC, marker=secondary_marker)
        df = pd.read_csv(background_C, delimiter=delimiter, engine = 'python')
        df.drop(columns=df.columns[0], axis=1, inplace=True)
        df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
        df.columns = df.columns.map(float)
        data = df.to_numpy()
        columns = df.columns.to_numpy()
        ax3.plot(columns, data[0], '--', linewidth=1.5, label=background_C_label + " A", color=secondaryA, marker=secondary_marker)
        ax3.plot(columns, data[1], '--', linewidth=1.5, label=background_C_label + " B", color=secondaryB, marker=secondary_marker)
        ax3.plot(columns, data[2], '--', linewidth=1.5, label=background_C_label + " C", color=secondaryC, marker=secondary_marker)

    
    if enable_legend:
        ax2.legend(loc=axis_loc)
        ax3.legend(loc=axis_loc)
    ax2.set_yticks([0,.2,.4,.6,.8,1],labels=[0.0,.2,.4,.6,.8,1.0],fontsize=12)
    ax2.set_xticks([0,.25,.5,.75,1,1.25,1.5,1.75,2],labels=['0.00',.25,'0.50',.75,'1.00',1.25,'1.50',1.75,'2.00'],fontsize=12)
    ax3.set_yticks([0,.2,.4,.6,.8,1],labels=[0.0,.2,.4,.6,.8,1.0],fontsize=12)
    ax3.set_xticks([0,.25,.5,.75,1,1.25,1.5,1.75,2],labels=['0.00',.25,'0.50',.75,'1.00',1.25,'1.50',1.75,'2.00'],fontsize=12)

# Creates a graph labeling system that works with a single graph or multiple graphs
fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel('Time (ps)', **{'size':14})
plt.ylabel('Average Population', labelpad=y_pad, **{'size':14})

plt.show()