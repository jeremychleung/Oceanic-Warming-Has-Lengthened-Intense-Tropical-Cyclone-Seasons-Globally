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
#rcParams['mathtext.fontset'] = 'stix'
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.fallback'] = 'stix'
rcParams['mathtext.default'] = 'regular'

#%%
oceanbasin = ['NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

#%%
bcolors = ['#8ECFC9','#FFBE7A','#FA7F6F','#82B0D2']
bcolors = ['r','b','k','grey']

fig,ax = plt.subplots(1,1,figsize=(9,3.5))
fig.subplots_adjust(left=0.08, bottom=0.20, right=0.98, top=0.90)

ax.axvspan(0.5,4.5,facecolor='lightskyblue', alpha=0.3)
ax.axvspan(4.5,6.5,facecolor='orchid', alpha=0.3)

for pp in [0,2]:
    df = pd.read_csv('alpha_itc.'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False)

    if pp==0:
        oblist = ['EP','WP','SI','SP']
        for iob,ob in enumerate(oblist):
            sr = df.loc[ob]

            slope = sr['dNdt']*10
            right = sr['Sum_term']*10
            Aterm = sr['A_term']*10
            Tterm = sr['T_term']*10

            pval = sr['p_dNdt']
            pval1 = sr['p_dAdt']
            pval2 = sr['p_dTdt']

            x = np.array([0.7,0.9,1.1,1.3])+iob
            y = np.array([Aterm, Tterm, right, slope])
            z = np.array([pval1, pval2, np.nan, pval])

            bb = ax.bar(x,y, width=0.15, color=bcolors, edgecolor='k', linewidth=0.4)

            print(pp,ob,y)
            yprob = y/slope*100
            print(pp,ob,[f'{iy:7.2f}%' for iy in yprob])
    elif pp==2:
        oblist = ['NA','WP']
        for iob,ob in enumerate(oblist,start=4):
            sr = df.loc[ob]

            slope = sr['dNdt']*10
            right = sr['Sum_term']*10
            Aterm = sr['A_term']*10
            Tterm = sr['T_term']*10

            pval = sr['p_dNdt']
            pval1 = sr['p_dAdt']
            pval2 = sr['p_dTdt']

            x = np.array([0.7,0.9,1.1,1.3]) + iob
            y = np.array([Aterm, Tterm, right, slope])
            z = np.array([pval1, pval2, np.nan, pval])

            bb = ax.bar(x,y, width=0.15, color=bcolors, edgecolor='k', linewidth=0.4)

            print(pp,ob,y)
            yprob = y/slope*100
            print(pp,ob,[f'{iy:7.2f}%' for iy in yprob])

ax.set_xticks(range(1,7))
ax.set_xticklabels(['ENP','WNP','SI','SP','NA','WNP'])
ax.set_xticks([0.5,4.5,6.5], minor=True)
ax.tick_params(which='major',length=3)
ax.tick_params(which='minor',length=17, top=True)

ax.axhline(0,0,1, color='gray', linestyle='--')
for iob in range(6):
    ax.axvline(1.5+iob,0,1, color='gray', linestyle='-', linewidth=0.4)

ax.tick_params(labelsize=16)
ax.set_ylabel('Trend [/dec]', fontsize=16)

ax.text(0.26,1.03,'Pre-season', fontdict={'weight':'normal', 'size':18}, transform=ax.transAxes)
ax.text(0.74,1.03,'Post-season', fontdict={'weight':'normal', 'size':18}, transform=ax.transAxes)

ax.set_xlim([0.5,6.5])

#------------------------
#legend
ax.legend(bb, [r'$\Delta{\alpha}/\Delta{t}$',
               r'$\Delta{TCG}/\Delta{t}$',
               r'$\Delta{\alpha}/\Delta{t}+\Delta{TCG}/\Delta{t}$',
               r'$\Delta{N}/\Delta{t}$'], loc=(0.10,-0.28),
          handletextpad=0.5, labelspacing=1, columnspacing=2.5, handlelength=2.5, handleheight=1.3, frameon=False, prop={'size':13}, ncols=4)
ax.set_xlim([0.5,6.5])

ymin,ymax = ax.get_ylim()
ylen = ymax - ymin
ax.set_ylim([ymin,ymin+1.5*ylen])

ax.text(-0.05,1.00,chr(107), fontdict={'weight':'bold','size':25}, transform=ax.transAxes)

#%%
fig.savefig('alpha_itc.png', dpi=600)
plt.show()