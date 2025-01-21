# -*- coding: utf-8 -*-
"""
Created on Fri Dec 13 22:12:02 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
import pymannkendall as mk
import statsmodels.api as sm
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
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.fallback'] = 'stix'
rcParams['mathtext.default'] = 'regular'


#%%
CKCD = 0.9
VREDUC = 0.8

oceanbasin = ['NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

for pp in [0,1]:
    mpi = pd.read_csv('../MPI/term_ratio/vmax_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    rat = pd.read_csv('../MPI/term_ratio/rat_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    ksk = pd.read_csv('../MPI/term_ratio/ksk_area_wgt'+f'{pp:1d}'+'.csv', index_col=0, keep_default_na=False, na_values=[' ',''])

    years = mpi.index.values
    yrbeg = years[0]
    yrend = years[-1]
    for iob,ob in enumerate(oceanbasin):
        impi = mpi[ob].values
        irat = rat[ob].values
        iksk = ksk[ob].values

        irat = irat - 1

        mpibar = np.nanmean(impi)
        ratbar = np.nanmean(irat)
        kskbar = np.nanmean(iksk)

        const = VREDUC**2*CKCD/(2*mpibar)

        impi_rat = VREDUC*np.sqrt(CKCD*irat*kskbar)
        impi_ksk = VREDUC*np.sqrt(CKCD*ratbar*iksk)

        #======================================================================
        fig,ax = plt.subplots(1,1,figsize=(5,2))
        fig.subplots_adjust(left=0.13, bottom=0.235, right=0.98, top=0.98)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        #-----------------------------------------------
        x = years
        y = impi
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        X = sm.add_constant(xs)
        model = sm.OLS(ys,X).fit()

        X = sm.add_constant(xs)
        pred = model.get_prediction(X)
        ci = pred.conf_int()

        ax.plot(xs,ci[:,0], linestyle='none', marker='.', markersize=4, color='grey', markerfacecolor='grey', markeredgewidth=0, alpha=0.6)
        ax.plot(xs,ci[:,1], linestyle='none', marker='.', markersize=4, color='grey', markerfacecolor='grey', markeredgewidth=0, alpha=0.6)
        ax.fill_between(xs, ci[:,0], ci[:,1], color='grey', alpha=0.2)

        slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)
        res = mk.original_test(y)
        pvalue = res.p

        if pvalue < 0.01:
            pval = '***'
        elif pvalue < 0.05:
            pval = '**'
        elif pvalue < 0.10:
            pval = '*'
        else:
            pval = ''

        mpi_reg = f'({slope*10:+.2f}'+r'm $s^{-1}$'+f'/dec{pval:s})'
        #-----------------------------------------------
        x = years
        y = impi_rat
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        X = sm.add_constant(xs)
        model = sm.OLS(ys,X).fit()

        X = sm.add_constant(xs)
        pred = model.get_prediction(X)
        ci = pred.conf_int()

        ax.plot(xs,ci[:,0], linestyle='none', marker='.', markersize=4, color='b', markerfacecolor='b', markeredgewidth=0, alpha=0.6)
        ax.plot(xs,ci[:,1], linestyle='none', marker='.', markersize=4, color='b', markerfacecolor='b', markeredgewidth=0, alpha=0.6)
        ax.fill_between(xs, ci[:,0], ci[:,1], color='b', alpha=0.2)

        slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)
        res = mk.original_test(y)
        pvalue = res.p

        if pvalue < 0.01:
            pval = '***'
        elif pvalue < 0.05:
            pval = '**'
        elif pvalue < 0.10:
            pval = '*'
        else:
            pval = ''

        mpi_rat_reg = f'({slope*10:+.2f}'+r'm $s^{-1}$'+f'/dec{pval:s})'
        #-----------------------------------------------
        x = years
        y = impi_ksk
        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        X = sm.add_constant(xs)
        model = sm.OLS(ys,X).fit()

        X = sm.add_constant(xs)
        pred = model.get_prediction(X)
        ci = pred.conf_int()

        ax.plot(xs,ci[:,0], linestyle='none', marker='.', markersize=4, color='r', markerfacecolor='r', markeredgewidth=0, alpha=0.6)
        ax.plot(xs,ci[:,1], linestyle='none', marker='.', markersize=4, color='r', markerfacecolor='r', markeredgewidth=0, alpha=0.6)
        ax.fill_between(xs, ci[:,0], ci[:,1], color='r', alpha=0.2)

        slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)
        res = mk.original_test(y)
        pvalue = res.p

        if pvalue < 0.01:
            pval = '***'
        elif pvalue < 0.05:
            pval = '**'
        elif pvalue < 0.10:
            pval = '*'
        else:
            pval = ''

        mpi_ksk_reg = f'({slope*10:+.2f}'+r'm $s^{-1}$'+f'/dec{pval:s})'

        #-----------------------------------------------
        l1, = ax.plot(years,impi, color='grey', linewidth=3)
        l2, = ax.plot(years,impi_rat, color='b', linewidth=3)
        l3, = ax.plot(years,impi_ksk, color='r', linewidth=3)

        ax.legend([l1,l2,l3],['MPI'+mpi_reg,r'MPI$_{\eta}$'+mpi_rat_reg,r'MPI$_{L}$'+mpi_ksk_reg],
                  loc=(0.48,-0.02), ncols=1, handletextpad=0.5, labelspacing=0.0, columnspacing=1.0, handlelength=2.5, handleheight=1.4, prop={'size':12}, frameon=False)

        ax.set_xticks(np.arange(1980,2030,10))
        ax.set_xticks(np.arange(1980,2030,2), minor=True)

        ax.tick_params(labelsize=14)
        ax.set_xlabel('Year', fontsize=16, labelpad=2)
        ax.set_ylabel(r'MPI [m $s^{-1}$]', fontsize=16, labelpad=2)

        ax.set_xlim([yrbeg,yrend])

        fig.savefig('mpi_term_area_ts.'+ob.lower()+f'{pp:1d}'+'.png', dpi=600)
        plt.show()
        plt.close()