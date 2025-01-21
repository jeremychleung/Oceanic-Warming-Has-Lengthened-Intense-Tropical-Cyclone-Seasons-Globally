# -*- coding: utf-8 -*-
"""
Created on Tue Sep 10 17:15:45 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
import pymannkendall as mk
from scipy import stats

#%%
yrbeg = 1980
yrend = 2023
years = np.arange(yrbeg,yrend+1)
nyear = years.size

ibtdf = pd.read_csv('../DataSet/ibtracs_lmi_time_leapyear.csv', index_col=0, keep_default_na=False)

season = pd.read_csv('../DataSet/ibtracs_itc_p5_p95.csv', index_col=0, keep_default_na=False, na_values='')
ssmean = season.mean(axis=0, skipna=True)

#%%
oceanbasin = ['NH','SH','NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

colnames = [x.lower()+str(y) for x in oceanbasin for y in [0,1,2]]

TSs = np.zeros([nyear,nbasin*3], dtype=np.int16)
ITCs = np.zeros([nyear,nbasin*3], dtype=np.int16)

TSs = pd.DataFrame(data=TSs, index=years, columns=colnames)
ITCs = pd.DataFrame(data=ITCs, index=years, columns=colnames)

cond0 = ibtdf['sshs'] >= 0
cond1 = ibtdf['sshs'] >= 4

for iob,ob in enumerate(oceanbasin):
    p05 = ssmean[ob.lower()+'05']
    p95 = ssmean[ob.lower()+'95']

    if ob == 'NH':
        cond2 = ibtdf['basin'].isin(['NA','EP','WP'])
    elif ob == 'SH':
        cond2 = ibtdf['basin'].isin(['SI','SP'])
    else:
        cond2 = ibtdf['basin'] == ob

    for iyr,yr in enumerate(years):
        cond3 = (ibtdf['season'] >= yr-1) & (ibtdf['season'] <= yr+1)

        #----------------------------------------------------------------------
        #pre-season
        cond4 = ibtdf['occurtime'] <= p05
        cond = cond0 & cond2 & cond3 & cond4
        TSs.loc[yr,ob.lower()+'0'] = cond.sum()
        cond = cond1 & cond2 & cond3 & cond4
        ITCs.loc[yr,ob.lower()+'0'] = cond.sum()

        #in-season
        cond4 = (ibtdf['occurtime'] > p05) & (ibtdf['occurtime'] < p95)
        cond = cond0 & cond2 & cond3 & cond4
        TSs.loc[yr,ob.lower()+'1'] = cond.sum()
        cond = cond1 & cond2 & cond3 & cond4
        ITCs.loc[yr,ob.lower()+'1'] = cond.sum()

        #post-season
        cond4 = ibtdf['occurtime'] >= p95
        cond = cond0 & cond2 & cond3 & cond4
        TSs.loc[yr,ob.lower()+'2'] = cond.sum()
        cond = cond1 & cond2 & cond3 & cond4
        ITCs.loc[yr,ob.lower()+'2'] = cond.sum()

#TSdf = pd.DataFrame(data=TSs, index=years, columns=colnames)
#TSdf.to_csv('Count_TSs.csv', index=True)

#ITCdf = pd.DataFrame(data=ITCs, index=years, columns=colnames)
#ITCdf.to_csv('Count_ITCs.csv', index=True)

#%%
for pp in [0,2]:
    regcoef = pd.DataFrame(index=oceanbasin, columns=['dNdt','T_bar','A_term','A_bar','T_term','Sum_term','p_dNdt','p_dAdt','p_dTdt'])

    for iob,ob in enumerate(oceanbasin):
        TCG = TSs[ob.lower()+f'{pp:1d}']
        N = ITCs[ob.lower()+f'{pp:1d}']
        Alpha = N/TCG

        if any(TCG==0): Warning('TCG is wrong!')

        #dN/dt = TCG_bar*dAlpha/dt + Alpha_bar*dTCG/dt

        T_bar = TCG.mean(skipna=True)
        A_bar = Alpha.mean(skipna=True)

        #----------------------------------------------------------------------
        #d(Alpha)/dt
        x = years
        y = Alpha
        slope1, intercept1, rvalue1, pvalue1, std_err1 = stats.linregress(x,y)
        dAdt = slope1

        res = mk.original_test(y,alpha=0.05)
        pvalue1 = res.p

        #----------------------------------------------------------------------
        #dTCG/dt
        x = years
        y = TCG
        slope2, intercept2, rvalue2, pvalue2, std_err2 = stats.linregress(x,y)
        dTdt = slope2

        res = mk.original_test(y,alpha=0.05)
        pvalue2 = res.p

        #----------------------------------------------------------------------
        x = years
        y = N
        slope, intercept, rvalue, pvalue, std_err = stats.linregress(x,y)
        dNdt = slope

        res = mk.original_test(y,alpha=0.05)
        pvalue = res.p

        #----------------------------------------------------------------------
        A_term = T_bar*dAdt
        T_term = A_bar*dTdt
        Sum_term = A_term + T_term

        regcoef.iloc[iob,:] = [dNdt,T_bar,A_term,A_bar,T_term,Sum_term,pvalue,pvalue1,pvalue2]
        #print(pp,ob,Ab)

    regcoef.to_csv('alpha_itc.'+f'{pp:1d}'+'.csv', index=True, float_format='%.2f')