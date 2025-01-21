# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:39:01 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd

#%%
yrsrt = 1980
yrend = 2023
years = np.arange(yrsrt,yrend+1)
nyear = years.size

ibtdf = pd.read_csv('ibtracs_lmi_time_leapyear.csv', index_col='sid', keep_default_na=False)

#%%
oceanbasin = ['NH','SH','NA','EP','WP','NI','SI','SP']
nbasin = len(oceanbasin)

prcts = np.array([5,95])
nprct = prcts.size

prct_glb = np.full([nyear,0], fill_value=np.nan)
colnames = []

cond1 = ibtdf['sshs'] >= 0  #TS+

for iob,ob in enumerate(oceanbasin):
    print(iob,ob)

    if ob == 'NH':
        cond2 = ibtdf['basin'].isin(['NA','EP','WP'])
    elif ob == 'SH':
        cond2 = ibtdf['basin'].isin(['SI','SP'])
    else:
        cond2 = ibtdf['basin'] == ob

    #--------------------------------------------------------------------------
    prct_ob = np.full([nyear,nprct], fill_value=np.nan)

    for iprct,prct in enumerate(prcts):
        colnames.append(f'{ob.lower()}{int(prct):02d}')

    for iyr,yr in enumerate(years):
        cond3 = (ibtdf['season'] >= yr-1) & (ibtdf['season'] <= yr+1)
        cond = cond1 & cond2 & cond3

        temp = ibtdf[cond]
        if temp.shape[0] == 0: continue

        for iprct,prct in enumerate(prcts):
            prct_ob[iyr,iprct] = np.percentile(temp['occurtime'].values, prct)

    prct_glb = np.hstack((prct_glb, prct_ob))

#%%
dfout = pd.DataFrame(data=prct_glb, index=years, columns=colnames)
dfout.to_csv('ibtracs_ts_p5_p95.csv', index=True)