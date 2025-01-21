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
oceanbasin = ['NA','WP']
nbasin = len(oceanbasin)

df = pd.read_csv('dgpi_area_wgt_term_trend.csv', index_col=0, keep_default_na=False)

#%%
bcolors = ['#8ECFC9','#FFBE7A','#FA7F6F','#82B0D2']
bcolors = ['g','y','r','b','k','grey']

for pp in [1]:
    for iob,ob in enumerate(oceanbasin):
        sr = df.loc[ob+f'{pp:1d}']

        left = sr['DGPI_trend']*10
        right = sr['ABCD_trend']*10
        aterm = sr['A_trend']*10
        bterm = sr['B_trend']*10
        cterm = sr['C_trend']*10
        dterm = sr['D_trend']*10

        x = np.array([1,2,3,4,5,6])
        y = np.array([aterm, bterm, cterm, dterm, right, left])

        fig,ax = plt.subplots(1,1,figsize=(5.5,3.7))
        fig.subplots_adjust(left=0.15, bottom=0.06, right=0.98, top=0.62)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        bb = ax.bar(x,y, width=0.5, align='center', color=bcolors, edgecolor='k', linewidth=0.4)

        print(pp,ob,[f'{x:.2f}%' for x in y[:4]/left*100])

        ax.legend(bb, [r'$\Delta{V_{s}}/\Delta{t}$',r'$\Delta{U_{y}}/\Delta{t}$',r'$\Delta{\omega}/\Delta{t}$',
                       r'$\Delta{\zeta_{a}}/\Delta{t}$',r'$\Delta{V_{s}}/\Delta{t}+\Delta{U_{y}}/\Delta{t}+\Delta{\omega}/\Delta{t}+\Delta{\zeta_{a}}/\Delta{t}$',r'$\Delta{DGPI}/\Delta{t}$'],
                  loc=(-0.19,1.10), prop={'size':16}, ncols=2, handletextpad=0.5,
                  labelspacing=0.7, columnspacing=1.3, handlelength=2.2, handleheight=1.4, frameon=False)

        ymin,ymax = ax.get_ylim()
        ylen = ymax - ymin

        ax.axhline(0,0,1, color='gray', linestyle='-', linewidth=0.8)
        ax.set_xticks(x)
        ax.set_xticklabels([])
        ax.tick_params(labelsize=17)

        ax.set_xlim([0.7,6.3])
        if pp==1:
            ax.set_ylim([ymin,ymax+0.1*ylen])
        else:
            ax.set_ylim([ymin,ymax+0.1*ylen])

        ax.text(-0.18,0.20,'Trend [/dec]', fontsize=19, rotation=90, transform=ax.transAxes)

        fig.savefig('dgpi_area_wgt_term_trend.'+ob.lower()+f'{pp:1d}'+'.png', dpi=600)
        plt.show()