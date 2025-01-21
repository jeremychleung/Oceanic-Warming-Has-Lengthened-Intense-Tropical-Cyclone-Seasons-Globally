# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 11:18:08 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
from scipy import stats

CKCD = 0.9
VREDUC = 0.8

oceanbasin = ['NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

termceof = pd.DataFrame(columns=['mpi_trend','ksk+rat_trend','ksk_trend','rat_trend'])

for pp in range(2):
    mpi = pd.read_csv('vmax_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    rat = pd.read_csv('rat_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    ksk = pd.read_csv('ksk_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])

    years = mpi.index.values
    for iob,ob in enumerate(oceanbasin):
        impi = mpi[ob].values
        irat = rat[ob].values
        iksk = ksk[ob].values

        irat = irat - 1

        mpibar = np.nanmean(impi)
        ratbar = np.nanmean(irat)
        kskbar = np.nanmean(iksk)

        const = VREDUC**2*CKCD/(2*mpibar)

        #--------------------
        x = years
        y = impi
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        mpi_slope,intecept,rvalue,pvalue,se = stats.linregress(xs,ys)

        #--------------------
        x = years
        y = iksk
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        ksk_slope,intecept,rvalue,pvalue,se = stats.linregress(xs,ys)

        #--------------------
        x = years
        y = irat
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        rat_slope,intecept,rvalue,pvalue,se = stats.linregress(xs,ys)

        #--------------------
        ksk_term = const*ratbar*ksk_slope
        rat_term = const*kskbar*rat_slope

        right = ksk_term + rat_term

        print(pp,ob, mpi_slope, right)
        print('-'*50)

        termceof.loc[ob+f'{pp:1d}'] = [mpi_slope, right, ksk_term, rat_term]

#---------------------------
termceof.to_csv('bempi_area_wgt_term_trend.csv', index=True, float_format='%.5f')