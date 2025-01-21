# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 01:38:50 2024

@author: Jimmy Liu, UCAS&LZU
"""

import datetime
import numpy as np
import pandas as pd

ibt = pd.read_csv('./IBTrACS/ibtracs.ALL.list.v04r01.csv', low_memory=False, keep_default_na=False, na_values=' ',
                  usecols=['SID','SEASON','BASIN','ISO_TIME','IFLAG','USA_LAT','USA_LON','USA_WIND','USA_SSHS'])
ibt.drop(index=0,inplace=True)
ibt = ibt.astype({'SEASON':'int32','ISO_TIME':'datetime64[ns]','USA_LAT':'float32','USA_LON':'float32','USA_WIND':'float32','USA_SSHS':'int32'})

cond1 = ibt['ISO_TIME'].dt.hour%6 == 0   #6-hour intervals
cond2 = ibt['IFLAG'].str.startswith('O') #observed data
cond = cond1 & cond2
ibt = ibt[cond].reset_index(drop=True)

#%%
sids = list(set(ibt['SID']))
sids.sort()

df = pd.DataFrame(columns=['sid','basin','season','year','month','day','hour','lat','lon','lmi','sshs','occurtime'])

n_storm = len(sids)
for i,sid in enumerate(sids):
    tc = ibt[ibt['SID'] == sid].reset_index(drop=True)

    if tc['USA_WIND'].isnull().all(): continue

    lmi = tc['USA_WIND'].max()
    ind = np.where(tc['USA_WIND'] == lmi)[0][0]

    bs = tc['BASIN'][ind]
    yr = tc['ISO_TIME'].dt.year[ind]
    mo = tc['ISO_TIME'].dt.month[ind]
    dy = tc['ISO_TIME'].dt.day[ind]
    hr = tc['ISO_TIME'].dt.hour[ind]

    lat = tc['USA_LAT'][ind]
    lon = tc['USA_LON'][ind]
    sshs = tc['USA_SSHS'][ind]

    dt = datetime.datetime(yr,mo,dy,0,0,0)

    #north hemisphere
    if lat > 0:
        ss = yr
        if dt < datetime.datetime(yr,2,16,0,0,0):
            ss = yr-1
        ddt = datetime.datetime(yr,mo,dy,hr,0,0) - datetime.datetime(ss,2,16,0,0,0)
    #south hemisphere
    else:
        ss = yr
        if dt > datetime.datetime(yr,8,16,0,0,0):
            ss = yr+1
        ddt = datetime.datetime(yr,mo,dy,hr,0,0) - datetime.datetime(ss-1,8,16,0,0,0)

    dday = ddt.total_seconds()/(24*3600)
    print(f'sid:{sid:13s} wmax:{lmi:5.1f} occurtime:{dday:6.2f}')

    lmi = np.int32(lmi)
    temp = pd.DataFrame([[sid,bs,ss,yr,mo,dy,hr,lat,lon,lmi,sshs,dday]],\
                        columns=['sid','basin','season','year','month','day','hour','lat','lon','lmi','sshs','occurtime'])

    df = pd.concat([df,temp])

df.reset_index(drop=True, inplace=True)
df.to_csv('ibtracs_lmi_time_leapyear.csv', index=False)