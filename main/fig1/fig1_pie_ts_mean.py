# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 10:16:47 2024

@author: meteo
"""

import datetime
import numpy as np
import pandas as pd
import xarray as xr
from scipy import io,stats
from matplotlib import pyplot as plt

#%%
Xdts = pd.date_range(start='20220101',end='20230601',freq='D')
Xi = np.argwhere(Xdts.day==1).ravel()
X2pi = Xi[Xi<365]/365 * 2*np.pi

#%%
yrbeg = 1980
yrend = 2023
years = np.arange(yrbeg, yrend+1)
nyear = years.size

ibt_year = pd.read_csv(r'..\DataSet\ibtracs_ts_p5_p95.csv', index_col=0, keep_default_na=False, na_values='')
ibt_mean = ibt_year.mean(axis=0, skipna=True)

oceanbasin = ['NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

for iob,ob in enumerate(oceanbasin):
    t05 = ibt_year[ob.lower()+'05']
    t95 = ibt_year[ob.lower()+'95']

    #----------------------------------
    #begin in reconstructed time series
    p1_05 = t05[(t05.index >= 1980) & (t05.index <= 2001)].mean()
    p2_05 = t05[(t05.index >= 2002) & (t05.index <= 2023)].mean()

    #----------------------------------
    #end in reconstructed time series
    p1_95 = t95[(t95.index >= 1980) & (t95.index <= 2001)].mean()
    p2_95 = t95[(t95.index >= 2002) & (t95.index <= 2023)].mean()

    #----------------------------------
    if ob in ['NA','EP','WP']:
        dt0_0 = datetime.datetime(2022,2,16,0,0,0) + datetime.timedelta(days=p1_05)  #5% percentile in the first period
        dt0_1 = datetime.datetime(2022,2,16,0,0,0) + datetime.timedelta(days=p2_05)  #5% percentile in the second period
        dt1_0 = datetime.datetime(2022,2,16,0,0,0) + datetime.timedelta(days=p1_95)  #95% percentile in the first period
        dt1_1 = datetime.datetime(2022,2,16,0,0,0) + datetime.timedelta(days=p2_95)  #95% percentile in the second period
    elif ob in ['SI','SP']:
        dt0_0 = datetime.datetime(2022,8,16,0,0,0) + datetime.timedelta(days=p1_05)
        dt0_1 = datetime.datetime(2022,8,16,0,0,0) + datetime.timedelta(days=p2_05)
        dt1_0 = datetime.datetime(2022,8,16,0,0,0) + datetime.timedelta(days=p2_95)
        dt1_1 = datetime.datetime(2022,8,16,0,0,0) + datetime.timedelta(days=p2_95)


    #%%
    fig,ax = plt.subplots(1,1,figsize=(3,3),subplot_kw=dict(projection="polar"), facecolor='none')
    fig.subplots_adjust(left=0.11, bottom=0.11, right=0.89, top=0.89)
    ax.set_theta_direction(-1) # clock-wise
    ax.set_theta_offset(np.pi/2) # 0degree orientation

    ax.axvspan(0,2*np.pi,color='#E0EBF3',zorder=-1)

    #----------------------------------
    #first year
    cond0 = (Xdts.year == dt0_0.year) & (Xdts.month == dt0_0.month) & (Xdts.day == dt0_0.day)
    cond1 = (Xdts.year == dt1_0.year) & (Xdts.month == dt1_0.month) & (Xdts.day == dt1_0.day)
    x0 = np.argwhere(cond0)[0][0]/365 * 2*np.pi
    x1 = np.argwhere(cond1)[0][0]/365 * 2*np.pi
    wd = x1 - x0
    ax.bar(x0,0.3, bottom=0.4, width=wd, edgecolor='w', color='gray', linewidth=1, align="edge")

    #----------------------------------
    #last year
    cond0 = (Xdts.year == dt0_1.year) & (Xdts.month == dt0_1.month) & (Xdts.day == dt0_1.day)
    cond1 = (Xdts.year == dt1_1.year) & (Xdts.month == dt1_1.month) & (Xdts.day == dt1_1.day)
    x0 = np.argwhere(cond0)[0][0]/365 * 2*np.pi
    x1 = np.argwhere(cond1)[0][0]/365 * 2*np.pi
    wd = x1 - x0
    ax.bar(x0,0.3, bottom=0.7, width=wd, edgecolor='w', color='k', linewidth=1, align="edge")

    print(ob,dt0_0,dt1_0)
    print(ob,dt0_1,dt1_1)
    print(x0,x1,wd)

    #----------------------------------
    ax.set_xticks(X2pi)
    ax.set_xticklabels(['J','F','M','A','M','J','J','A','S','O','N','D'], fontdict={'weight':'bold'})
    ax.set_yticks([0.4,0.7,1])
    ax.tick_params(labelleft=False, pad=1.0, labelsize=25)
    ax.spines[:].set_linewidth(2)
    ax.set_rmax(1.0)
    ax.grid(visible=False)
    #ax.set_axis_off()

    fig.savefig('pie_ts.'+ob.lower()+'.png', dpi=600)
    plt.show()
    plt.close()