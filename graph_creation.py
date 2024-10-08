import pandas as pd
import matplotlib.pyplot as plt

################################################################
##  Generates an n-length column of connected graphs
## 
##  No major error checking is done, so make sure that the range of all
##  the files are roughly similar. Also, the length of all the data arrays
##  should be identical if they are enabled. 
################################################################

comparison = True # Whether to have the comparison background graph behind every graph
enable_legend = True # Whether to enable the graph legend
legend_loc = 1 # Where to put the legend in the graph
data_zorder = 2.5 # The order of the data on the graphs - <2 means than the secondary data should be in front

## Primary data files - solid line
datafiles = ['data/general/phasedamping.out', 'data/general/phasedamping-0.9-2.7-0.9.out', 'data/general/phasedamping-0.9-0.3-0.9.out']
datalabels = ['Deph.', 'Incr.', 'Decr.']

## Secondary data files - dashed line
secondarydata = ['data/general/nodamping.out', datafiles[0], datafiles[0]]
secondarydatalabels = ['Pure', datalabels[0], datalabels[0]]

## Leave blank for no markers - see https://matplotlib.org/stable/api/markers_api.html
secondary_marker = ''

## Color Scheme
maincolorA = '#2f0033'
maincolorB = '#0500b4'
maincolorC = '#ff0000'
secondaryA = '#664169'
secondaryB = '#8686ff'
secondaryC = '#ff5b5b'

y_pad = 7

## The regex delimiter used to get the data from the C2QA output
delimiter = '\s*\(|[\+-]\d\.\d+e[\+-]\d+j\) *\(|[\+-]\d\.\d+e[\+-]\d+j\)'

## Graph genreration
fig = plt.figure()
gs = fig.add_gridspec(len(datafiles), hspace=0)
axs = gs.subplots(sharex=True, sharey=True)

## Handles the case where there is only one input
if len(datafiles) == 1:
    axes = axs
    axs = []
    axs.append(axes)

## Iterates through all of the data files
for n in range(len(datafiles)):
    ## Read in data
    df = pd.read_csv(datafiles[n], delimiter=delimiter, engine = 'python')
    ## Drop first and last column, as they are blank (thanks to delimiter pattern used)
    df.drop(columns=df.columns[0], axis=1, inplace=True)
    df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
    df.columns = df.columns.map(float)
    data = df.to_numpy()
    columns = df.columns.to_numpy()
    ## Plot data
    axs[n].plot(columns, data[0], linewidth=1.5, label=datalabels[n] + " A", color=maincolorA, zorder=data_zorder)
    axs[n].plot(columns, data[1], linewidth=1.5, label=datalabels[n] + " B", color=maincolorB, zorder=data_zorder)
    axs[n].plot(columns, data[2], linewidth=1.5, label=datalabels[n] + " C", color=maincolorC, zorder=data_zorder)

    ## Displays the secondary data if comparison is True
    if comparison:
        df = pd.read_csv(secondarydata[n], delimiter=delimiter, engine = 'python')
        df.drop(columns=df.columns[0], axis=1, inplace=True)
        df.drop(columns=df.columns[len(df.columns)-1], axis=1, inplace=True)
        df.columns = df.columns.map(float)
        data = df.to_numpy()
        columns = df.columns.to_numpy()
        axs[n].plot(columns, data[0], '--', linewidth=1.5, label=secondarydatalabels[n] + " A", color=secondaryA, marker=secondary_marker)
        axs[n].plot(columns, data[1], '--', linewidth=1.5, label=secondarydatalabels[n] + " B", color=secondaryB, marker=secondary_marker)
        axs[n].plot(columns, data[2], '--', linewidth=1.5, label=secondarydatalabels[n] + " C", color=secondaryC, marker=secondary_marker)

    ## Displays the lenged if enable_legend is True
    if enable_legend:
        axs[n].legend(loc=legend_loc)
        axs[n].set_yticks([0,.2,.4,.6,.8,1],labels=[0.0,.2,.4,.6,.8,1.0],fontsize=12)
        axs[n].set_xticks([0,.25,.5,.75,1,1.25,1.5,1.75,2],labels=['0.00',.25,'0.50',.75,'1.00',1.25,'1.50',1.75,'2.00'],fontsize=12)

## Creates a graph labeling system that works with a single graph or multiple graphs
fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', which='both', top=False, bottom=False, left=False, right=False)
plt.xlabel('Time (ps)', **{'size':14})
plt.ylabel('Average Population', labelpad=y_pad, **{'size':14})

plt.show()