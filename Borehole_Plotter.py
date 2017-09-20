import matplotlib.gridspec as gridspec
import matplotlib.pyplot as pl
import pylab
from pandas import Series

# First bring in the borehole data, incorporating the selected constituents
cocs = ['uranium','nitrate','tritium']
my_data = {}
file = 'D:\\Composite_Log_Test\\199_N_184.csv'
with open(file, 'r') as data:
    for line in data:
        row = line.split(',')
        coc = row[5].lower()
        depth = 0
        if coc in cocs:
            if coc not in my_data.keys():
                my_data[coc] = {'so':{'depth':[],'data':[]},'gw':{'depth':[],'data':[]}}
            if row[53] != '' and row[54] != '':
                depth = (float(row[53]) + float(row[54]))/2
            elif row[54] != '':
                depth = float(row[54])
            elif row[53] != '':
                depth = float(row[53])
            if depth != 0:
                if 'l' in row[7].lower():
                    my_data[coc]['gw']['depth'].append(float(depth))
                    my_data[coc]['gw']['data'].append(float(row[6]))
                else:
                    my_data[coc]['so']['depth'].append(float(depth))
                    my_data[coc]['so']['data'].append(float(row[6]))

# Create a list of series to plot
plot_list = []
for key in my_data.keys():
    for media in my_data[key].keys():
        plot = Series(
            data=my_data[key][media]['data'],
            index=my_data[key][media]['depth'],
            name=str(key+'_'+media))
        plot = plot.sort_values('index')
        plot_list.append(plot)

rows = 4
cols = 12

fig = pylab.figure(figsize=(8, 6))
g_main = gridspec.GridSpec(rows, cols)
# Slug Test Table Test
columns = ['Date', 'Static Water\nLevel (ft bgs)', 'Slug Vol.\n(ft3)', 'Screen Interval',
           'Representative\nHydraulic Conductivity (m/d)']
row_label = ['Slug Test\nResults']
contents = [['Sep 16, 2017', 60, 0.1, '50 - 50.5', 1000]]
table_test = fig.add_subplot(g_main[3:, 7:])
table_test.set_xticks([])
table_test.set_yticks([])
table_test.set_frame_on(False)
pylab.table(cellText=contents,colLabels=columns,rowLabels=row_label,colWidths=[0.18]*6,loc='center')
location = pl.subplot(g_main[0:2, :4])
pl.xticks(())
pl.yticks(())
location_string = str('E 571,430.74 m E N 149,817.82 m NAD83(91)\n' +
                      'Ground Surface Elevation (brass cap): 140.528 m NAD83\n' +
                      'Total Depth = 108 ft Below Ground Surface (bgs)\n' +
                      'Type of Drilling Rig: Cable Tool w/Drive Barrel'
                      )

pl.text(0.01, 0.95, location_string, ha='left', va='top', size=5.8)
title = pl.subplot(g_main[0, 4:8])
pl.xticks(())
pl.yticks(())
title_string = str('199-N-184 C8186')
pl.text(0.5, 0.5, title_string, ha='center', va='center', size=16)
for i in range(cols):
    my_plot = pl.subplot(g_main[2, i])
    pl.xticks(())
    pl.yticks(())
    try:
        my_plot.plot(plot_list[i])
        pl.gca().invert_xaxis()
    except:
        pl.text(0.5, 0.5, str('#' + str(i+1)), ha='center', rotation='vertical', va='center', size=24, alpha=.5)
axes_footer = pl.subplot(g_main[3:, :6])
pl.xticks(())
pl.yticks(())
pl.text(0.5, 0.5, 'Footer', ha='center', va='center', size=24, alpha=.5)
pl.tight_layout()
pl.show()

'''
footer_sub = gridspec.GridSpecFromSubplotSpec(2, 6, subplot_spec=g_main[3, 7:])

x = [[1,2],[2,1]]
fig_test = pylab.figure()
g_main = gridpsec.GridSpec(rows,cols)
table_test = fig_test.add_subplot(g_main[3:, 7:])
table_test.set_xticks([])
table_test.set_yticks([])
table_test.set_frame_on(False)
pylab.table(cellText=x,colLabels=['col']*2,rowLabels=['row']*2,colWidths=[0.3]*2,loc='center')
'''