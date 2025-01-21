# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 11:18:08 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
import pymannkendall as mk
from scipy import stats

oceanbasin = ['NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

termceof = pd.DataFrame(columns=['DGPI_trend','ABCD_trend','A_trend','B_trend','C_trend','D_trend'])

for pp in range(2):
    DGPI = pd.read_csv('dgpi_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    A = pd.read_csv('a_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    B = pd.read_csv('b_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    C = pd.read_csv('c_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    D = pd.read_csv('d_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    #A: vertical wind shear
    #B: zonal wind meridional gradient at 500 hPa
    #C: vertical velocity at 500 hPa
    #D: abs vorticity at 500 hPa

    BCD = pd.read_csv('bcd_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    ACD = pd.read_csv('acd_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    ABD = pd.read_csv('abd_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    ABC = pd.read_csv('abc_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])

    years = DGPI.index.values
    for iob,ob in enumerate(oceanbasin):
        dgpi = DGPI[ob].values
        a = A[ob].values
        b = B[ob].values
        c = C[ob].values
        d = D[ob].values

        bcd = BCD[ob].values
        acd = ACD[ob].values
        abd = ABD[ob].values
        abc = ABC[ob].values

        bcd_bar = np.nanmean(bcd)
        acd_bar = np.nanmean(acd)
        abd_bar = np.nanmean(abd)
        abc_bar = np.nanmean(abc)

        #----------------------------------------------------------------------
        x = years
        y = dgpi
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        dgpi_slope,intecept,rvalue,pvalue,se = stats.linregress(xs,ys)
        res = mk.original_test(y)
        pvalue = res.p

        #----------------------------------------------------------------------
        x = years
        y = a
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        a_slope,intecept,rvalue,pvalue,se = stats.linregress(xs,ys)
        res = mk.original_test(y)
        pvalue = res.p

        #----------------------------------------------------------------------
        x = years
        y = b
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        b_slope,intecept,rvalue,pvalue,se = stats.linregress(xs,ys)
        res = mk.original_test(y)
        pvalue = res.p

        #----------------------------------------------------------------------
        x = years
        y = c
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        c_slope,intecept,rvalue,pvalue,se = stats.linregress(xs,ys)
        res = mk.original_test(y)
        pvalue = res.p

        #----------------------------------------------------------------------
        x = years
        y = d
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        d_slope,intecept,rvalue,pvalue,se = stats.linregress(xs,ys)
        res = mk.original_test(y)
        pvalue = res.p

        #----------------------------------------------------------------------
        a_term = a_slope*bcd_bar*np.exp(-11.8)
        b_term = b_slope*acd_bar*np.exp(-11.8)
        c_term = c_slope*abd_bar*np.exp(-11.8)
        d_term = d_slope*abc_bar*np.exp(-11.8)

        right = a_term + b_term + c_term + d_term

        print(pp,ob, dgpi_slope, right)

        termceof.loc[ob+f'{pp:1d}'] = [dgpi_slope, right, a_term, b_term, c_term, d_term]

#------------------------------------------------------------------------------
termceof.to_csv('dgpi_area_wgt_term_trend.csv', index=True, float_format='%.6f')