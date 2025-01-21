# -*- coding: utf-8 -*-
"""
Created on Sat Dec 14 22:27:03 2024

@author: Jimmy Liu, UCAS&LZU
"""

import cmaps
import numpy as np
import pandas as pd
import pymannkendall as mk
from scipy import stats
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
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
Ndts = pd.date_range('20220216','20230215',freq='D')
Sdts = pd.date_range('20220816','20230815',freq='D')
N1st = np.argwhere(Ndts.day==1).ravel()
S1st = np.argwhere(Sdts.day==1).ravel()
Nlab = ['Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb']
Slab = ['Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']

#%%
yrsrt = 1980
yrend = 2023
years = np.arange(yrsrt,yrend+1)
nyear = years.size

ibtdf = pd.read_csv('../DataSet/ibtracs_lmi_time_leapyear.csv', index_col=0, keep_default_na=False)

#%%
oceanbasin = ['NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

prct = np.array([0,1,2,3,4,5,6,7,8,9,10,90,91,92,93,94,95,96,97,98,99,100])
nprct = prct.size
colnames = [f'p{pp:d}' for pp in prct]

ITC = dict()

cond4 = ibtdf['sshs'] >= 4

for iob,ob in enumerate(oceanbasin):
    cond1 = ibtdf['basin'] == ob

    ITCyr = np.full([nyear,nprct], fill_value=np.nan)
    for iyr,yr in enumerate(years):
        cond2 = (ibtdf['season'] >= yr-1) & (ibtdf['season'] <= yr+1)
        cond = cond4 & cond1 & cond2
        if ibtdf[cond].shape[0] == 0: continue
        for ipp,pp in enumerate(prct):
            ITCyr[iyr,ipp] = np.percentile(ibtdf[cond]['occurtime'].values, pp)

    temp = np.full([nyear,int(nprct/2)], fill_value=np.nan)
    for icol in range(int(nprct/2)):
        print(icol,int(nprct/2)+icol,int(nprct/2)-icol-1)
        temp[:,icol] = ITCyr[:,int(nprct/2)+icol] - ITCyr[:,int(nprct/2)-icol-1]

    ITCyr = pd.DataFrame(temp, index=years, columns=[f'd{x:d}' for x in range(0,11)[::-1]])
    ITC[ob.lower()] = ITCyr



#%%
fig,axs = plt.subplots(5,1,figsize=(7,14),sharex=True)
fig.subplots_adjust(left=0.09, bottom=0.045, right=0.88, top=0.965, wspace=0.21, hspace=0.30)

rgb = plt.get_cmap(cmaps.MPL_gist_rainbow).colors
rgb = np.array(rgb)[::10,:]
rgb = np.delete(rgb,[7,8], axis=0)

for iob,ob in enumerate(oceanbasin):
    ax = axs[iob]
    ax.spines[:].set_linewidth(1.1)
    ax.tick_params(which='major', length=4, width=1.1)
    ax.text(-0.07,1.05,chr(97+iob), fontdict={'weight':'bold','size':29}, transform=ax.transAxes)

    df = ITC[ob.lower()]

    x = df.index.values
    for idd,dd in enumerate(range(0,11)[::-1]):
        y = df[f'd{dd:d}'].values

        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        slope, intercept, rvalue, pvalue_ls, std_err = stats.linregress(xs,ys)
        res = mk.original_test(y)
        pvalue = res.p
        if pvalue < 0.01:
            pval = '<0.01'
        elif pvalue < 0.05:
            pval = '<0.05'
        elif pvalue < 0.10:
            pval = '<0.10'
        else:
            pval = f'={pvalue:.2f}'

        #print(ob,pp,slope*10,pvalue)
        print(f'{ob:2s}, {dd:2d}, slope:{slope*10:4.1f}d/dec, t-test:{pvalue_ls:.3f}, mk-test:{pvalue:.3f}')

        lc = rgb[idd,:]

        ax.plot(x,y, color=lc, linewidth=1)

        if pp == 95:
            ax.text(0.0, 1.20, f'95th: {slope*10:+.2f}d/dec, p{pval:s}', fontdict={'weight':'normal','size':14}, transform=ax.transAxes)
        elif pp == 5:
            ax.text(0.0, 1.02, f'5th:   {slope*10:+.2f}d/dec, p{pval:s}', fontdict={'weight':'normal','size':14}, transform=ax.transAxes)

    for idd,dd in enumerate(range(0,11)[::-1]):
        y = df[f'd{dd:d}'].values

        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)
        yfit = years*slope + intercept

        lc = rgb[idd,:]

        ax.plot(years, yfit, color=lc, linestyle='--', linewidth=3)

    ax.set_xticks(np.arange(1980,2030,2), minor=True)
    ax.set_xticks(np.arange(1980,2030,10))

    ymin,ymax = ax.get_ylim()
    ylen = ymax - ymin
    if ob in ['NA','EP','WP']:
        if ylen>=250:
            ax.set_yticks(N1st, minor=True)
            ax.set_yticks(N1st[::2])
            ax.set_yticklabels(Nlab[::2])
        else:
            ax.set_yticks(N1st)
            ax.set_yticklabels(Nlab)
    elif ob in ['SI','SP']:
        if ylen>=250:
            ax.set_yticks(S1st, minor=True)
            ax.set_yticks(S1st[::2])
            ax.set_yticklabels(Slab[::2])
        else:
            ax.set_yticks(S1st)
            ax.set_yticklabels(Slab)
    ax.set_ylim([ymin,ymax])
    ax.set_xlim([1980,2022])

    ax.tick_params(labelsize=15)

    if ob == 'SP':
        ax.set_xlabel('Year', fontsize=20, labelpad=3)

    obtxt = ob
    if ob == 'EP':
        obtxt = 'ENP'
    elif ob == 'WP':
        obtxt = 'WNP'

    ax.set_title(obtxt, loc='right', fontdict={'weight':'normal', 'size':18}, pad=2)

cmap = mcolors.ListedColormap(rgb)
norm = mcolors.Normalize(vmin=1, vmax=nprct/2+1)
im = cm.ScalarMappable(norm=norm, cmap=cmap)

right = axs[2].get_position().x1
top = axs[0].get_position().y1
bot = axs[4].get_position().y0
axc = (top - bot)/2
cbh = 0.7
cbw = 0.035
cax = fig.add_axes([0.91,0.15,cbw,cbh])
cb = fig.colorbar(im, cax=cax)
cb.ax.set_yticks(np.arange(1,nprct/2+1))
cb.ax.set_yticks(np.arange(1,nprct/2+1)+0.5, minor=True)
cb.ax.set_yticklabels([])
cb.ax.set_yticklabels(['90th-10th','91th-9th','92th-8th','93th-7th','94th-6th','95th-5th',
                       '96th-4th','97th-3rd','98th-2nd','99th-1st','First-Last'], minor=True,va='center', fontsize=13, rotation=90)
cb.ax.tick_params(which='major', length=17, tickdir='in')

#----------------------------------------
fig.savefig('figs4_len.png', dpi=600)
plt.show()