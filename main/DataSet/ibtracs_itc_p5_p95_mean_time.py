# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 09:05:52 2024

@author: Jimmy Liu, UCAS&LZU
"""

import datetime
import numpy as np
import pandas as pd

#%%
yrbeg = 1982
yrend = 2023
years = np.arange(yrbeg, yrend+1)
nyear = years.size

season = pd.read_csv('ibtracs_itc_p5_p95.csv', index_col=0, keep_default_na=False, na_values='')
ssmean = season.mean(axis=0, skipna=True)

#%%
lat = np.arange(-90,90.1,2.5)
lon = np.arange(0,360,2.5)
ny = lat.size
nx = lon.size

oceanbasin = ['NH','SH','NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

for iob,ob in enumerate(oceanbasin):
    p05 = ssmean[ob.lower()+'05']
    p95 = ssmean[ob.lower()+'95']
    plen = p95 - p05

    if ob in ['NH','NA','EP','WP']:
        dt0 = datetime.datetime(2022,2,16,0,0,0) + datetime.timedelta(days=p05)
        dt1 = datetime.datetime(2022,2,16,0,0,0) + datetime.timedelta(days=p95)
    elif ob in ['SH','SI','SP']:
        dt0 = datetime.datetime(2021,8,16,0,0,0) + datetime.timedelta(days=p05)
        dt1 = datetime.datetime(2021,8,16,0,0,0) + datetime.timedelta(days=p95)

    print(ob,f'{dt0:%m%d}', f'{dt1:%m%d} {plen:5.1f} ')