# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 11:29:06 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Helvetica'
rcParams['xtick.top'] = 'False'
rcParams['ytick.right'] = 'False'
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'
rcParams['hatch.color'] = 'k'
rcParams['hatch.linewidth'] = 0.6
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.fallback'] = 'stix'
rcParams['mathtext.default'] = 'regular'

#%%
oceanbasin = ['NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

df = pd.read_csv('../MPI/term_ratio/bempi_area_wgt_term_trend.csv', index_col=0, keep_default_na=False)

#%%
bcolors = ['#8ECFC9','#FFBE7A','#FA7F6F','#82B0D2']
bcolors = ['r','b','k','grey']

fig,ax = plt.subplots(1,1,figsize=(13,3.2))
fig.subplots_adjust(left=0.045, bottom=0.09, right=0.69, top=0.90)

ax.axvspan(0.5,4.5,facecolor='lightskyblue', alpha=0.3)
ax.axvspan(4.5,5.5,facecolor='orchid', alpha=0.3)

for pp in [0,1]:
    if pp==0:
        oblist = ['EP','WP','SI','SP']
        for iob,ob in enumerate(oblist):
            sr = df.loc[ob+f'{pp:1d}']

            slope = sr['mpi_trend']*10
            right = sr['ksk+rat_trend']*10
            Kterm = sr['ksk_trend']*10
            Rterm = sr['rat_trend']*10

            x = np.array([0.7,0.9,1.1,1.3])+iob
            y = np.array([Kterm, Rterm, right, slope])

            bb = ax.bar(x,y, width=0.15, color=bcolors, edgecolor='k', linewidth=0.4)

            print(pp, ob, y)
            print(pp, ob, [f'{yy/slope*100:.3f}%' for yy in y])
    elif pp==1:
        oblist = ['NA']
        for iob,ob in enumerate(oblist,start=4):
            sr = df.loc[ob+f'{pp:1d}']

            slope = sr['mpi_trend']*10
            right = sr['ksk+rat_trend']*10
            Kterm = sr['ksk_trend']*10
            Rterm = sr['rat_trend']*10

            x = np.array([0.7,0.9,1.1,1.3]) + iob
            y = np.array([Kterm, Rterm, right, slope])

            bb = ax.bar(x,y, width=0.15, color=bcolors, edgecolor='k', linewidth=0.4)

            print(pp, ob, y)
            print(pp, ob, [f'{yy/slope*100:.3f}%' for yy in y])

ax.set_xticks(range(1,6))
ax.set_xticklabels(['ENP','WNP','SI','SP','NA'])
ax.set_xticks([0.5,4.5,5.5], minor=True)
ax.tick_params(which='major',length=3)
ax.tick_params(which='minor',length=17, top=True)

ax.axhline(0,0,1, color='gray', linestyle='--')
for iob in range(6):
    ax.axvline(1.5+iob,0,1, color='gray', linestyle='-', linewidth=0.4)

ax.tick_params(labelsize=17)
ax.set_ylabel('Trend [/dec]', fontsize=19)

ax.text(0.330,1.03,'Pre-season', fontdict={'weight':'normal', 'size':20}, transform=ax.transAxes)
ax.text(0.811,1.03,'Post-season', fontdict={'weight':'normal', 'size':20}, transform=ax.transAxes)

#------------------------
#legend
ax.legend(bb, ['','       ','       ',''], loc=(1.02,0.30), prop={'size':14},
          handletextpad=0.5, labelspacing=2, columnspacing=1.0, handlelength=2.5, handleheight=1.4, frameon=False, ncols=4)

ax.text(1.03,0.47,r'$\Delta{L}/\Delta{t}$',fontsize=16, transform=ax.transAxes)
ax.text(1.12,0.47,r'$\Delta{\eta}/\Delta{t}$',fontsize=16, transform=ax.transAxes)
ax.text(1.21,0.47,r'$\Delta{L}/\Delta{t}+\Delta{\eta}/\Delta{t}$',fontsize=16, transform=ax.transAxes)
ax.text(1.38,0.47,r'$\Delta{MPI}/\Delta{t}$',fontsize=16, transform=ax.transAxes)

ax.set_xlim([0.5,5.5])

ymin,ymax = ax.get_ylim()
ylen = ymax - ymin
ax.set_ylim([ymin,ymin+1.1*ylen])

ax.text(-0.07,1.00,chr(97), fontdict={'weight':'bold','size':33}, transform=ax.transAxes)

#%%
fig.savefig('mpi_term_ratio.png', dpi=600)
plt.show()