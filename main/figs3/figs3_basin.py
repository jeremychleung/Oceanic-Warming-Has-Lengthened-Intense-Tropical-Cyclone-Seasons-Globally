# -*- coding: utf-8 -*-
"""
Created on Tue Jun  4 16:54:33 2024

@author: Jimmy Liu, UCAS&LZU
"""

import cmaps
import calendar
import numpy as np
import pandas as pd
import matplotlib as mpl
from scipy import stats
from matplotlib import ticker
from matplotlib import pyplot as plt
from matplotlib.colors import ListedColormap
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

NHdt = pd.date_range(start='2022-02-16', end='2023-02-15', freq='D')
NHx = np.argwhere(NHdt.day == 1).ravel()
NHmo = ['Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb']

SHdt = pd.date_range(start='2022-07-16', end='2023-07-15', freq='D')
SHx = np.argwhere(SHdt.day == 1).ravel()
SHmo = ['Aug','Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul']

#%%
yrbeg = 1980
yrend = 2023
years = np.arange(yrbeg,yrend+1)
nyear = years.size

nrun = 9
nyrbeg = yrbeg + (nrun-1)/2
nyrend = yrend - (nrun-1)/2
nyears = np.arange(nyrbeg,nyrend+1)
nnyear = nyears.size

rgb = plt.get_cmap(cmaps.BlAqGrYeOrReVi200).colors
rgb = np.array(rgb)
ind = np.arange(rgb.shape[0])[0:195:5]
nrgb = rgb[ind,:]
ncmap = ListedColormap(nrgb)

df = pd.read_csv('../DataSet/ibtracs_lmi_time_leapyear.csv', keep_default_na=False)

season = pd.read_csv('../DataSet/ibtracs_itc_p5_p95.csv', index_col=0, keep_default_na=False, na_values='')
ssmean = season.mean(axis=0, skipna=True)

#%%
oceanbasin = ['NH','SH','NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

cond1 = df['sshs'] >= 4

for iob,ob in enumerate(oceanbasin):
    p05 = ssmean[ob.lower()+'05']
    p95 = ssmean[ob.lower()+'95']
    print(ob,p05,p95)

    x = np.floor(p05/5)
    y = (p05 - x*5)/5
    xp05 = x+y

    x = np.floor(p95/5)
    y = (p95 - x*5)/5
    xp95 = x+y

    if ob == 'NH':
        cond2 = df['basin'].isin(['NA','EP','WP'])
    elif ob == 'SH':
        cond2 = df['basin'].isin(['SI','SP'])
    else:
        cond2 = df['basin'] == ob

    #--------------------------------------------------------------------------
    fig,axs = plt.subplots(2,1,figsize=(8,3.8), height_ratios=[1.3,1], sharex=True)
    fig.subplots_adjust(left=0.07, bottom=0.20, right=0.94, top=0.90, hspace=0)

    for iax in axs:
        iax.spines[:].set_linewidth(1.5)

    ax = axs[0]
    in_axes = fig.add_axes([0.72,0.66,0.21,0.22])

    for i in range(2):
        if i==0:
            cond3 = (df['season'] >= 1980) & (df['season'] <= 2001)
        else:
            cond3 = (df['season'] >= 2002) & (df['season'] <= 2023)

        cond = cond1 & cond2 & cond3

        df0 = df[cond].reset_index(drop = True)

        dint = np.arange(1,74,1)
        dint_count = np.zeros(dint.size)

        ptimes = df0['occurtime'].values/5
        pp= [int(np.floor(x) + 1) for x in ptimes]

        for ix,x in enumerate(dint):
            dint_count[ix] = pp.count(x)
        tol = np.sum(dint_count)

        cc = 'royalblue' if i==0 else 'r'
        ax.bar(dint*5-0.70+i*1.4, dint_count, width=1.4, color=cc, alpha=1,
               label='1980-2001' if i==0 else '2002-2023')

        #gaussian kde
        kernel = stats.gaussian_kde(ptimes, bw_method=1)
        K = kernel(dint)
        K = K/np.sum(K)*tol

        ax.plot(dint*5, K, color=cc, linestyle='--', linewidth=2)

        in_axes.plot(dint*5, K, color=cc, linestyle='--', linewidth=2)


    ax.tick_params(labelsize=15)
    ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))

    ax.text(-0.08,0.30,'Count', fontsize=16, transform=ax.transAxes, rotation=90)
    obtxt = ob
    if ob == 'EP':
        obtxt = 'ENP'
    elif ob == 'WP':
        obtxt = 'WNP'
    ax.set_title(obtxt, loc='right', fontsize=17)

    ax.axhline(1, 0, 1, color='gray', linestyle='--', linewidth=1)
    ax.axvline(p05, 0, 1, color='lime', linestyle='--', linewidth=3)
    ax.axvline(p95, 0, 1, color='lime', linestyle='--', linewidth=3)

    ax.legend(loc='upper left', prop={'size':14})

    #inserted axes
    in_axes.set_yscale('log', base=np.e)

    in_axes.set_xticks(np.arange(0,74,6)[1:]*5)
    in_axes.set_xticklabels([])

    ytiks = [-2., -1.,  0.,  1.,  2.]
    ylabs = [r'e$^{-2}$','',r'e$^{0}$','',r'e$^{2}$']
    in_axes.set_yticks(np.exp(ytiks))
    in_axes.set_yticklabels(ylabs)
    in_axes.set_ylim([0.1,15])

    in_axes.tick_params(bottom=False, labelsize=13)

    in_axes.axhline(1,0,1, color='gray', linestyle='--', linewidth=1.5)

    figind = iob if ob in ['NH','SH'] else iob-2
    ax.text(-0.07,1.01,chr(97+figind), fontdict={'weight':'bold','size':36}, transform=ax.transAxes)

    #--------------------------------------------------------------------------
    ax = axs[1]

    day_samples = np.arange(0,366,2)
    nday = day_samples.size

    for iyr,yr in enumerate(nyears):
        cond3 = df['season'].isin(np.arange(yr-3,yr+4))
        cond = cond1 & cond2 & cond3

        df0 = df[cond].reset_index(drop = True)

        kernel = stats.gaussian_kde(df0['occurtime'].values, bw_method='scott')
        print(ob,yr,kernel.factor)
        K = kernel(day_samples)
        K = K/np.sum(K)*100
        if K.max() >= 10:
            K[:] = np.nan

        ax.plot(day_samples, K, color=nrgb[iyr,:], linestyle='-', linewidth=1.5, alpha=0.5)

    cb_axes = fig.add_axes([0.835,0.25,0.040,0.180])
    norm = mpl.colors.Normalize(vmin=nyrbeg, vmax=nyrend)
    cb = fig.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=ncmap), cax=cb_axes, orientation='vertical')
    cb.ax.set_yticks([nyrbeg,nyrend])
    cb.ax.tick_params(labelsize=12)
    cb.ax.set_title('Year', pad=3, fontsize=12)


    cc = ['#1868B2', '#DE582B']
    for i in range(2):
        if i==0:
            cond4 = (season.index >= 1980) & (season.index <= 2001)
        else:
            cond4 = (season.index >= 2002) & (season.index <= 2023)
        ip05 = season[cond4][ob.lower()+'05'].mean(axis=0, skipna=True)
        ip95 = season[cond4][ob.lower()+'95'].mean(axis=0, skipna=True)

        if i==0:
            l1 = ax.axvline(ip05, 0,1,color=cc[i], linewidth=3, linestyle='--', label='1980-2001')
            ax.axvline(ip95, 0,1,color=cc[i], linewidth=3, linestyle='--', label='1980-2001')
        else:
            l2 = ax.axvline(ip05, 0,1,color=cc[i], linewidth=3, linestyle='--', label='2002-2023')
            ax.axvline(ip95, 0,1,color=cc[i], linewidth=3, linestyle='--', label='2002-2023')

    ax.legend([l1,l2],[l1.get_label(),l2.get_label()], loc='upper left', prop={'size':14})

    ymin,ymax = ax.get_ylim()

    ax.set_yticks(np.arange(0,20))
    ax.set_ylim([0,ymax])

    ax.tick_params(left=False, labelleft=False, right=True, labelright=True, labelsize=14)

    if ob in ['NH','NA','EP','WP']:
        ax.set_xticks(NHx)
        ax.set_xticklabels([])
        if ob in ['NH','WP']:
            ax.set_xticklabels(NHmo, fontsize=16)
    elif ob in ['SH','SP','SI']:
        ax.set_xticks(SHx)
        ax.set_xticklabels([])
        if ob in ['SH','SP']:
            ax.set_xticklabels(SHmo, fontsize=16)

    ax.text(1.04,0.04,'PDF [%]', fontsize=14, rotation=90, transform=ax.transAxes)
    print('-'*30)

    #--------------------------------------------------------------------------
    fig.savefig('count_pdf.'+ob.lower()+'.png', dpi=600)
    plt.show()