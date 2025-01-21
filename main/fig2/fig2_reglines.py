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

prct = np.array([1,2,3,4,5,6,7,8,9,10,15,20,25,30,35,40,45,50,55,60,65,70,75,80,85,90,91,92,93,94,95,96,97,98,99])
nprct = prct.size
colnames = [f'p{pp:d}' for pp in prct]

TS = dict()
ITC = dict()

cond0 = ibtdf['sshs'] >= 0
cond4 = ibtdf['sshs'] >= 4

for iob,ob in enumerate(oceanbasin):
    cond1 = ibtdf['basin'] == ob

    #------------------------------------------------
    TSyr = np.full([nyear,nprct], fill_value=np.nan)
    for iyr,yr in enumerate(years):
        cond2 = (ibtdf['season'] >= yr-1) & (ibtdf['season'] <= yr+1)
        cond = cond0 & cond1 & cond2
        if ibtdf[cond].shape[0] == 0: continue
        for ipp,pp in enumerate(prct):
            TSyr[iyr,ipp] = np.percentile(ibtdf[cond]['occurtime'].values, pp)

    #------------------------------------------------
    ITCyr = np.full([nyear,nprct], fill_value=np.nan)
    for iyr,yr in enumerate(years):
        cond2 = (ibtdf['season'] >= yr-1) & (ibtdf['season'] <= yr+1)
        cond = cond4 & cond1 & cond2
        if ibtdf[cond].shape[0] == 0: continue
        for ipp,pp in enumerate(prct):
            ITCyr[iyr,ipp] = np.percentile(ibtdf[cond]['occurtime'].values, pp)

    TSyr = pd.DataFrame(TSyr, index=years, columns=colnames)
    ITCyr = pd.DataFrame(ITCyr, index=years, columns=colnames)

    TS[ob.lower()] = TSyr
    ITC[ob.lower()] = ITCyr

#%%
fig,axs = plt.subplots(5,2,figsize=(11,14),sharex=True)
fig.subplots_adjust(left=0.06, bottom=0.045, right=0.84, top=0.955, wspace=0.21, hspace=0.40)

rgb = plt.get_cmap(cmaps.MPL_gist_rainbow).colors
rgb = np.array(rgb)[::3,:]
rgb = np.delete(rgb,[18,19,20,21,22,23,24,25], axis=0)

#newcmap = LinearSegmentedColormap.from_list('mycmap', rgb, N=20)

rgb2 = plt.get_cmap(cmaps.BlAqGrYeOrRe).colors
rgb2 = np.array(rgb2)[::1,:]
for iob,ob in enumerate(oceanbasin):
    for icol in range(2):
        ax = axs[iob,icol]
        ax.spines[:].set_linewidth(1.1)
        ax.tick_params(which='major', length=4, width=1.1)
        ax.text(-0.13,1.08,chr(97+iob*2+icol), fontdict={'weight':'bold','size':32}, transform=ax.transAxes)

        df = ITC[ob.lower()] if icol==0 else TS[ob.lower()]

        x = df.index.values
        for ipp,pp in enumerate(prct):
            y = df[f'p{pp:1d}'].values

            ind = ~np.isnan(y)
            xs = x[ind]
            ys = y[ind]

            slope, intercept, rvalue, pvalue1, std_err = stats.linregress(xs,ys)
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

            if pp in [5,50,95]:
                #print(ob,icol,pp,slope*10,pvalue1,pvalue)
                print(f'{ob:2s}, col:{icol:1d}, pct:{pp:2d}%, slope:{slope*10:5.1f}d/dec, t-test:{pvalue1:.3f}, mk-test:{pvalue:.3f}')

            lc = rgb[ipp,:]

            ax.plot(x,y, color=lc, linewidth=1)

            if pp == 95:
                ax.text(0.0, 1.23, f'95th: {slope*10:+.2f}d/dec, p{pval:s}', fontdict={'weight':'normal','size':16}, transform=ax.transAxes)
            elif pp == 50:
                ax.text(0.0, 1.13, f'50th: {slope*10:+.2f}d/dec, p{pval:s}', fontdict={'weight':'normal','size':16}, transform=ax.transAxes)
            elif pp == 5:
                ax.text(0.0, 1.02, f'5th:   {slope*10:+.2f}d/dec, p{pval:s}', fontdict={'weight':'normal','size':16}, transform=ax.transAxes)

        for pp in [5,50,95]:
            y = df[f'p{pp:1d}'].values

            ind = ~np.isnan(y)
            xs = x[ind]
            ys = y[ind]

            slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)

            yfit = years*slope + intercept
            ax.plot(years, yfit, color='k', linestyle='--', linewidth=3)

            if icol==1:
                ypos = 2023*slope + intercept
                ax.text(2022.8,ypos-7, f'{pp}th', fontsize=17)

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

        ax.tick_params(labelsize=18)

        if ob == 'SP':
            ax.set_xlabel('Year', fontsize=23, labelpad=2)

cmap = mcolors.ListedColormap(rgb)
norm = mcolors.Normalize(vmin=1, vmax=36)
im = cm.ScalarMappable(norm=norm, cmap=cmap)

right = axs[0,1].get_position().x1
top = axs[0,0].get_position().y1
bot = axs[4,0].get_position().y0
axc = (top - bot)/2
cbh = 0.7
cbw = 0.032
cax = fig.add_axes([0.90,0.12,cbw,cbh])
cb = fig.colorbar(im, cax=cax)
cb.ax.set_yticks(np.arange(1,36))
cb.ax.set_yticks(np.arange(1,36)+0.5, minor=True)
cb.ax.set_yticklabels([])
cb.ax.set_yticklabels([f'{y:d}' for y in prct], minor=True, fontsize=16)
cb.ax.tick_params(which='major', length=25, tickdir='in')
cb.ax.set_ylabel('Percentile',fontsize=22,labelpad=6)

#----------------------------------------
fig.savefig('fig2_reglines.png', dpi=600)
plt.show()