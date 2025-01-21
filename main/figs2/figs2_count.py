# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:54:33 2024

@author: Jimmy Liu, UCAS&LZU
"""

import calendar
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
rcParams['mathtext.fontset'] = 'stix'
rcParams['mathtext.default'] = 'regular'

#%%
mo_abbr = []
for i in range(1,13):
    mo_abbr.append(calendar.month_abbr[i])
mo_abbr = np.array(mo_abbr)
mo_abbr = np.array(['J','F','M','A','M','J','J','A','S','O','N','D'])

#%%
yrbeg = 1980
yrend = 2023
years = np.arange(yrbeg,yrend+1)
nyear = years.size

ibtdf = pd.read_csv('../DataSet/ibtracs_lmi_time_leapyear.csv', index_col=0, keep_default_na=False)

#%%
fig,axs = plt.subplots(3,3,figsize=(9,6), sharex=False)
fig.subplots_adjust(left=0.06, bottom=0.06, right=0.99, top=0.96, wspace=0.18, hspace=0.35)

#==============================================================================
for irow in [0,2]:
    for icol in range(3):
        axs[irow,icol].spines[:].set_visible(False)
        axs[irow,icol].tick_params(bottom=False, left=False, labelbottom=False, labelleft=False)

x0 = axs[0,0].get_position().x0
x1 = axs[0,0].get_position().x1
y0 = axs[0,0].get_position().y0
y1 = axs[0,0].get_position().y1
xw = x1 - x0
yw = y1 - y0

dd = axs[1,1].get_position().x0 - axs[1,0].get_position().x1
#==============================================================================

cond0 = ibtdf['sshs'] >= 0
cond4 = ibtdf['sshs'] >= 4
cond1 = ibtdf['season'].isin(years)

for iob,ob in enumerate(['NH','SH','NA','EP','WP','SI','SP']):
    if ob in ['NH','SH']:
        if ob == 'NH':
            ax = fig.add_axes([x0+0.084,y0,xw*1.3,yw])
            xn = ax.get_position().x1
        else:
            ax = fig.add_axes([xn+dd,y0,xw*1.3,yw])
    elif ob in ['NA','EP','WP']:
        ax = axs[1,iob-2]
    else:
        ax = axs[2,iob-5]
        x0 = ax.get_position().x0
        x1 = ax.get_position().x1
        y0 = ax.get_position().y0
        y1 = ax.get_position().y1
        ax = fig.add_axes([x0+0.164,y0,x1-x0,y1-y0])

    if ob == 'NH':
        cond2 = ibtdf['basin'].isin(['NA','EP','WP'])
    elif ob == 'SH':
        cond2 = ibtdf['basin'].isin(['SI','SP'])
    else:
        cond2 = ibtdf['basin'] == ob

    #---------------------------
    #TS
    cond = cond0 & cond1 & cond2

    df0 = ibtdf[cond].reset_index(drop=True)
    mo_col = df0['month'].value_counts()
    for mo in range(1,13):
        if mo not in mo_col.index:
            mo_col[mo] = 0
    mo_col0 = mo_col.sort_index()

    #---------------------------
    #Intense TC
    cond = cond4 & cond1 & cond2

    df4 = ibtdf[cond].reset_index(drop=True)
    mo_col = df4['month'].value_counts()
    for mo in range(1,13):
        if mo not in mo_col.index:
            mo_col[mo] = 0
    mo_col4 = mo_col.sort_index()

    if ob in ['NH','NA','EP','WP']:
        ind = [2,3,4,5,6,7,8,9,10,11,12,1]
    else:
        ind = [8,9,10,11,12,1,2,3,4,5,6,7]

    bar0 = ax.bar(np.arange(1,13),mo_col0[ind].values,width=0.65,color='b',edgecolor='none',linewidth=0.5, label='TS+', alpha=1)
    bar4 = ax.bar(np.arange(1,13),mo_col4[ind].values,width=0.45,color='r',edgecolor='none',linewidth=0.5, label='CAT4-5', alpha=1)
    ind = np.array(ind)

    ax.legend([bar0,bar4],['TS+','ITC'],loc='upper left',prop={'size':8})

    ax.set_xticks(np.arange(1,13))
    ax.set_xticklabels(mo_abbr[ind-1])
    ax.tick_params(bottom=False, labelsize=9, pad=1)

    if ob in ['SI','SP']:
        ax.set_xlabel('Month', fontsize=11, labelpad=1.0)

    if ob in ['NH','NA','SI']:
        ax.set_ylabel('Count', fontsize=11, labelpad=1.0)

    obtxt = ob
    if ob == 'WP':
        obtxt = 'WNP'
    elif ob == 'EP':
        obtxt = 'ENP'
    if ob in ['EP','WP']:
        ax.text(0.82,0.85,obtxt,fontsize=11,transform=ax.transAxes)
    else:
        ax.text(0.89,0.85,obtxt,fontsize=11,transform=ax.transAxes)

    ax.set_xlim([0.4,12.6])

    ax.text(-0.10,1.025,chr(97+iob),fontdict={'weight':'bold','size':19},transform=ax.transAxes)

#---------------------------------------
fig.savefig('figs2_count.png', dpi=600)