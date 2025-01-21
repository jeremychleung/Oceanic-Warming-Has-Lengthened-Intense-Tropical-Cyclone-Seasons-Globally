# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 19:54:13 2024

@author: Jimmy Liu, UCAS&LZU
"""

import cmaps
import numpy as np
import pandas as pd
import matplotlib.patches as patches
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
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
ibt = pd.read_csv('../DataSet/IBTrACS/ibtracs.ALL.list.v04r01.csv', low_memory=False, keep_default_na=False, na_values=' ',
                  usecols=['SID','SEASON','BASIN','ISO_TIME','IFLAG','USA_LAT','USA_LON','USA_WIND','USA_SSHS'])
ibt.drop(index=0,inplace=True)
ibt = ibt.astype({'SEASON':'int32','ISO_TIME':'datetime64[ns]','USA_LAT':'float32','USA_LON':'float32','USA_WIND':'float32','USA_SSHS':'int32'})

cond1 = ibt['ISO_TIME'].dt.hour%6 == 0   #6-hour intervals
cond2 = ibt['IFLAG'].str.startswith('O')    #observed data
cond3 = ibt['SEASON'] >= 1978
cond = cond1 & cond2 & cond3
ibt = ibt[cond].reset_index(drop=True)

#%%
yrbeg = 1980
yrend = 2023
years = np.arange(yrbeg,yrend+1)
nyear = years.size

TSs = pd.read_csv('../DataSet/ibtracs_lmi_time_leapyear.csv', index_col=0, keep_default_na=False)
cond1 = TSs['season'].isin(years)
cond2 = TSs['sshs'] >= 0
cond = cond1 & cond2
TSs = TSs[cond]

season = pd.read_csv('../DataSet/ibtracs_itc_p5_p95.csv', index_col=0, keep_default_na=False, na_values='')
ssmean = season.mean(axis=0, skipna=True)

basingeo = np.load('../DataSet/BasinPolygon/basin.npy', allow_pickle=True)

#%%
oceanbasin = ['NA','EP','WP','SI','SP']

fig,axs = plt.subplots(3,1,figsize=(3.9,7))
fig.subplots_adjust(left=0.06, bottom=0.08, right=0.94, top=0.96, wspace=0.06, hspace=0.15)

rgb = plt.get_cmap(cmaps.seaice_1).colors
sshs_colors = np.array(rgb)[[1,2,5,3,8,9],:]
sshs_colors[4,:] = np.array([255,120,120])/255.0
sshs_colors[5,:] = np.array([255,0,0])/255.0
sshs_cate = ['TS','CAT1','CAT2','CAT3','CAT4','CAT5']

titles = ['Pre-season','In-season','Post-season']
for pp in range(3):
    ax = axs[pp]

    m = Basemap(projection='robin', lon_0=200, resolution='c', ax=ax)
    m.fillcontinents(color='#B2B3B7',lake_color='w')
    m.drawparallels([-90,-40,0,40,90], labels=[1,1,0,0], linewidth=0.5, fontsize=9)
    m.drawmeridians(np.arange(0,361,90), labels=[0,0,0,1], linewidth=0.5, fontsize=9, yoffset=150000)

    lat = [79.0,79.0]
    lon = [0,359.9]
    mx,my = m(lon,lat)
    m.plot([19.99,20], [89.3,89.3], color='k', linewidth=1.2, latlon=True)
    m.plot([19.99,20], [-89.3,-89.3], color='k', linewidth=1.2, latlon=True)

    for i in range(len(sshs_colors)):
        x0 = 0.190+i*0.1097
        rect = patches.Rectangle((x0,0.03),0.075,0.030, facecolor=sshs_colors[i], edgecolor='k', linewidth=1, transform=fig.transFigure, fill=True)
        fig.add_artist(rect)
        plt.figtext(x0+0.014+(3-len(sshs_cate[i]))*0.008,0.040,sshs_cate[i], fontsize=7)

    ax.set_title(titles[pp], fontsize=12, pad=2)

    ax.text(0.0, 0.95, chr(pp+97), fontdict={'weight':'bold', 'size':18}, transform=ax.transAxes)

    #plot track
    for iob,ob in enumerate(oceanbasin):
        p05 = ssmean[ob.lower()+'05']
        p95 = ssmean[ob.lower()+'95']

        cond1 = TSs['basin'] == ob

        if pp == 0:
            cond2 = TSs['occurtime'] <= p05
        elif pp == 2:
            cond2 = TSs['occurtime'] >= p95
        else:
            cond2 = (TSs['occurtime'] > p05) & (TSs['occurtime'] < p95)
        cond = cond1 & cond2

        sid_ob = TSs[cond].index.values
        if len(sid_ob)==0: continue

        for sshs in [0,1,2,3,4,5]:
            for isid,sid in enumerate(sid_ob):
                tc = ibt[ibt['SID'] == sid].reset_index(drop=True)

                lat = tc['USA_LAT'].values
                lon = tc['USA_LON'].values
                sshss = tc['USA_SSHS'].values

                print(pp,ob,sshs,sid)

                lon[lon < 0] += 360

                n = lat.size
                for i in range(1,n):
                    if sshss[i] != sshs: continue
                    x0 = lon[i-1]
                    y0 = lat[i-1]

                    x1 = lon[i]
                    y1 = lat[i]
                    ic = sshss[i]+1
                    m.plot([x0,x1],[y0,y1], color=sshs_colors[sshs,:], linewidth=0.6, latlon=True, alpha=0.5)

        if pp==0:
            geo = basingeo.item()[f'{ob:s}{0:1d}']
            lat = geo['lat']
            lon = geo['lon']
            m.plot(lon, lat, color='k', linewidth=1, latlon=True)

            ax.text(0.81, 0.68, 'NA', fontdict={'weight':'normal', 'size':10}, transform=ax.transAxes)
            ax.text(0.60, 0.46, 'ENP', fontdict={'weight':'normal', 'size':10}, transform=ax.transAxes)
            ax.text(0.38, 0.61, 'WNP', fontdict={'weight':'normal', 'size':10}, transform=ax.transAxes)
            ax.text(0.50, 0.39, 'SP', fontdict={'weight':'normal', 'size':10}, transform=ax.transAxes)
            ax.text(0.20, 0.31, 'SI', fontdict={'weight':'normal', 'size':10}, transform=ax.transAxes)
        elif pp==2:
            geo = basingeo.item()[f'{ob:s}{1:1d}']
            lat = geo['lat']
            lon = geo['lon']
            m.plot(lon, lat, color='k', linewidth=1, latlon=True)

    m.drawcoastlines(linewidth=0.4)

#--------------------------------------
fig.savefig('figs1_robin.png', dpi=600)