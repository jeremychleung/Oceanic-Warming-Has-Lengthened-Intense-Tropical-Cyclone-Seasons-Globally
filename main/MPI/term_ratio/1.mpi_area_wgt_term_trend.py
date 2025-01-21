# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 11:18:08 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
import pymannkendall as mk
from scipy import stats

CKCD = 0.9
VREDUC = 0.8

oceanbasin = ['NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

termceof = pd.DataFrame(columns=['mpi_trend','fac+rat_trend','fac_trend','rat_trend'])

for pp in range(2):
    mpi = pd.read_csv('vmax_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    fac = pd.read_csv('fac_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    rat = pd.read_csv('rat_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])

    years = mpi.index.values
    for iob,ob in enumerate(oceanbasin):
        impi = mpi[ob].values
        ifac = fac[ob].values
        irat = rat[ob].values

        mpi_bar = np.nanmean(impi)
        fac_bar = np.nanmean(ifac)
        rat_bar = np.nanmean(irat)

        const = VREDUC**2*CKCD/(2*mpi_bar)

        #----------------------------------------------------------------------
        x = years
        y = impi
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        mpi_slope,intecept,rvalue,pvalue,se = stats.linregress(xs,ys)
        res = mk.original_test(y)
        pvalue = res.p

        #----------------------------------------------------------------------
        x = years
        y = ifac
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        fac_slope,intecept,rvalue,pvalue,se = stats.linregress(xs,ys)
        res = mk.original_test(y)
        pvalue = res.p

        #----------------------------------------------------------------------
        x = years
        y = irat
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        rat_slope,intecept,rvalue,pvalue,se = stats.linregress(xs,ys)
        res = mk.original_test(y)
        pvalue = res.p

        #----------------------------------------------------------------------
        fac_term = const*rat_bar*fac_slope
        rat_term = const*fac_bar*rat_slope

        right = fac_term + rat_term

        print(pp,ob, mpi_slope, right)

        termceof.loc[ob+f'{pp:1d}'] = [mpi_slope, right, fac_term, rat_term]

#---------------------------
termceof.to_csv('mpi_area_wgt_term_trend.csv', index=True, float_format='%.5f')