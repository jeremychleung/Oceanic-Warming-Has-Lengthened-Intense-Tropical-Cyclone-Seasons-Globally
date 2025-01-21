# -*- coding: utf-8 -*-
"""
Created on Wed Dec 18 22:48:32 2024

@author: Jimmy Liu, UCAS&LZU
"""

import cmaps
import numpy as np
import pymannkendall as mk
from scipy import stats
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
ulat = np.load('./data/ulat.npy', allow_pickle=True)
wlat = np.load('./data/wlat.npy', allow_pickle=True)

lons = ulat.item()['lon']
levels = ulat.item()['level'].astype(int)
years = ulat.item()['year']

nx = lons.size
nz = levels.size
nyear = years.size

X,Z = np.meshgrid(lons,levels)

#%%
oceanbasin = ['WP']
nbasin = len(oceanbasin)

for iob,ob in enumerate(oceanbasin):
    u = ulat.item()[ob.lower()+'1']
    w = wlat.item()[ob.lower()+'1']
    u = np.array(u)
    w = np.array(w)

    um = u.mean(axis=0)
    wm = w.mean(axis=0)

    trend = np.full([nz,nx], fill_value=np.nan)
    ptest = np.full([nz,nx], fill_value=np.nan)
    for iz,ilev in enumerate(levels):
        for ix,ilon in enumerate(lons):
            x = years
            y = w[:,iz,ix]

            ind = ~np.isnan(y)
            xs = x[ind]
            ys = y[ind]

            slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)
            res = mk.original_test(y)
            pvalue = res.p

            trend[iz,ix] = slope*10
            ptest[iz,ix] = pvalue

    wm *= 100   #Pa/s to hPa/s
    trend *= 100    #Pa/s to hPa/s

    print(ob, np.nanmin(trend), np.nanmax(trend))

    #--------------------------------------------------------------------------
    fig,ax = plt.subplots(1,1,figsize=(5,2))
    fig.subplots_adjust(left=0.10, bottom=0.11, right=0.87, top=0.97)
    ax.set_yscale('log', base=10, subs=[1])
    cint = np.arange(-1.2,1.21,0.2)
    cf = ax.contourf(X,Z,trend, levels=cint, cmap=cmaps.testcmap, extend='both')

    xz = np.where(ptest <=0.05)
    ax.plot(X[xz],Z[xz], marker='.', markersize=6, markeredgewidth=0.8, linestyle='none', color='gray', markerfacecolor='none', zorder=1)

    Q = ax.quiver(X,Z,um,-10*wm, scale=1.5, angles='uv', scale_units='xy', units='xy')

    ax.axvline(130,0,1, linestyle='--', color='k')
    ax.axvline(180,0,1, linestyle='--', color='k')

    ax.invert_yaxis()
    ax.set_xticks(np.arange(0,360.1,10), minor=True)
    ax.set_xticks(np.arange(0,360.1,30))
    xlabs = []
    for x in ax.get_xticks():
        if x%180 == 0:
            xlabs.append(f'{int(x):d}'+r'$\degree$')
        elif x<180:
            xlabs.append(f'{int(x):d}'+r'$\degree$E')
        else:
            xlabs.append(f'{int(360-x):d}'+r'$\degree$W')
    ax.set_xticklabels(xlabs)
    #ax.set_xticklabels([f'{int(x):d}'+r'$\degree$E' if x%180!=0 else f'{int(x):d}'+r'$\degree$' for x in ax.get_xticks()])

    ax.set_yticks(levels, minor=True)
    ax.set_yticks([1000,925,850,700,600,500,400,300,250,200,150,100])
    ax.set_yticklabels([f'{y:d}' for y in ax.get_yticks()])
    #ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%d"))
    ax.set_zorder(0)

    ax.tick_params(labelsize=8)
    ax.set_ylabel('Pressure [hPa]', fontsize=10, labelpad=1)

    ax.set_xlim([0,240])
    ax.set_ylim([1000,200])

    x1 = ax.get_position().x1
    y0 = ax.get_position().y0
    y1 = ax.get_position().y1
    cax = fig.add_axes([x1+0.018,y0,0.022,y1-y0])
    cb = fig.colorbar(cf, cax=cax, orientation='vertical')
    cb.ax.tick_params(labelsize=7)
    cb.ax.set_ylabel(r'Trend [$\times10^{-2}$'+'Pa s'+r'$^{-1}$/dec]', fontsize=7, labelpad=1.0)

    #--------------------------------------------------------------------------
    fig.savefig('figs6_uw_section.png', dpi=600)
    plt.show()
    plt.close()