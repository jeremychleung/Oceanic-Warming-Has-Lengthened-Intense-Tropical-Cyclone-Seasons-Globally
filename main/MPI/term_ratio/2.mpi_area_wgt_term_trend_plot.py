# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 13:09:38 2024

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

df = pd.read_csv('mpi_area_wgt_term_trend.csv', index_col=0, keep_default_na=False)

#%%
bcolors = ['#8ECFC9','#FFBE7A','#FA7F6F','#82B0D2']
bcolors = ['r','b','k','grey']

for pp in range(2):

    fig,ax = plt.subplots(1,1,figsize=(6,3))
    fig.subplots_adjust(left=0.10, bottom=0.10, right=0.98, top=0.90)

    for iob,ob in enumerate(oceanbasin):
        sr = df.loc[ob+f'{pp:1d}']

        left = sr['mpi_trend']*10
        right = sr['fac+rat_trend']*10
        fac_term = sr['fac_trend']*10
        rat_term = sr['rat_trend']*10

        x = np.array([0.7,0.9,1.1,1.3]) + iob
        y = np.array([fac_term, rat_term, right, left])
        bb = ax.bar(x,y, width=0.15, color=bcolors, edgecolor='k', linewidth=0.4)

        print(y)

    ax.legend(bb, [r'$\overline{RAT}\times\Delta{FAC}/\Delta{t}$',
                   r'$\overline{FAC}\times\Delta{RAT}/\Delta{t}$',
                   r'$\overline{RAT}\times\Delta{FAC}/\Delta{t}+\overline{FAC}\times\Delta{RAT}/\Delta{t}$',
                   r'$\Delta{MPI}/\Delta{t}$'], loc='upper left', prop={'size':8}, handletextpad=0.5)

    ymin,ymax = ax.get_ylim()
    ylen = ymax - ymin
    for iob in range(nbasin):
        ax.axvline(1.5+iob,0,1, color='gray', linestyle='-', linewidth=0.4)

    ax.axhline(0,0,1, color='gray', linestyle='--')
    ax.set_xticks(np.arange(1,nbasin+1,1))
    ax.set_xticklabels(oceanbasin)
    ax.set_xlim([0.5,nbasin+0.5])
    if pp==1:
        ax.set_ylim([ymin,ymax+0.09*ylen])
    else:
        ax.set_ylim([ymin,ymax+0.30*ylen])

    #ax.set_ylabel('Trend [/dec]', fontsize=12)
    ax.text(-0.11,0.32,'Trend [/dec]', fontsize=12, rotation=90, transform=ax.transAxes)
    ax.set_title('Pre-season' if pp==0 else 'Post-season', fontdict={'weight':'bold', 'size':14}, pad=2)

    fig.savefig('mpi_area_wgt_term_trend.'+f'{pp:1d}'+'.png', dpi=600)
    plt.show()