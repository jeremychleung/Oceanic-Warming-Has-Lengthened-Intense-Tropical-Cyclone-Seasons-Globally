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

df = pd.read_csv('dgpi_area_wgt_term_trend.csv', index_col=0, keep_default_na=False)

#%%
bcolors = ['#8ECFC9','#FFBE7A','#FA7F6F','#82B0D2']
bcolors = ['g','y','r','b','k','grey']

for pp in range(2):

    fig,ax = plt.subplots(1,1,figsize=(6,3))
    fig.subplots_adjust(left=0.10, bottom=0.10, right=0.98, top=0.90)

    ax.axvspan(0.5,1.5,facecolor='lightskyblue', alpha=0.3)
    ax.axvspan(2.5,3.5,facecolor='orchid', alpha=0.3)

    for iob,ob in enumerate(oceanbasin):
        sr = df.loc[ob+f'{pp:1d}']

        left = sr['DGPI_trend']*10
        right = sr['ABCD_trend']*10
        aterm = sr['A_trend']*10
        bterm = sr['B_trend']*10
        cterm = sr['C_trend']*10
        dterm = sr['D_trend']*10

        x = np.array([0.6,0.75,0.90,1.05,1.20,1.35]) + iob
        y = np.array([aterm, bterm, cterm, dterm, right, left])

        bb = ax.bar(x,y, width=0.12, color=bcolors, edgecolor='k', linewidth=0.4)

        print(y)

    ax.legend(bb, [r'$V_{s}$',r'$U_{y}$',r'$\omega$',r'$\zeta_{a}$',r'$V_{s}+U_{y}+\omega+\zeta_{a}$','DGPI'],
              loc='upper right', prop={'size':8}, ncols=2, handletextpad=0.5)

    ymin,ymax = ax.get_ylim()
    ylen = ymax - ymin
    for iob in range(nbasin):
        ax.axvline(1.5+iob,0,1, color='gray', linestyle='-', linewidth=0.4)

    ax.axhline(0,0,1, color='gray', linestyle='-', linewidth=0.8)
    ax.set_xticks(np.arange(1,nbasin+1,1))
    ax.set_xticklabels(['NA','ENP','WNP','SI','SP'])
    ax.set_xlim([0.5,nbasin+0.5])
    if pp==1:
        ax.set_ylim([ymin,ymax+0.001*ylen])
    else:
        ax.set_ylim([ymin,ymax+0.001*ylen])

    ax.text(-0.11,0.32,'Trend [/dec]', fontsize=12, rotation=90, transform=ax.transAxes)
    ax.set_title('Pre-season' if pp==0 else 'Post-season', fontdict={'weight':'bold', 'size':14}, pad=2)

    fig.savefig('dgpi_area_wgt_term_trend.'+f'{pp:1d}'+'.png', dpi=600)
    plt.show()