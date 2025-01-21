# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 13:09:38 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
import pymannkendall as mk
import statsmodels.api as sm
from scipy import stats
from matplotlib import ticker
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
oceanbasin = ['NA','WP']
nbasin = len(oceanbasin)

#%%
bcolors = ['#8ECFC9','#FFBE7A','#FA7F6F','#82B0D2']
bcolors = ['g','y','r','b','k','grey']
varphy = [r'$V_{shear}$',r'$du_{500}/dy$',r'$\omega_{500}$',r'$\zeta_{850}$']
varunit = [r'm $s^{-1}$',r'm $s^{-2}$',r'Pa $s^{-1}$',r'$s^{-1}$']

for ivar,varnm in enumerate(['aa','bb','cc','dd']):
    df = pd.read_csv(varnm+'_area_wgt1.csv', index_col=0, keep_default_na=False, na_values=[' ',''])
    years = df.index.values
    yrbeg = years[0]
    yrend = years[-1]

    if varnm == 'aa':
        coef = -1
    elif varnm == 'bb':
        coef = 5
    elif varnm == 'cc':
        coef = 2
    elif varnm == 'dd':
        coef = 5

    df = df * 10**coef

    for iob,ob in enumerate(oceanbasin):
        fig,ax = plt.subplots(1,1,figsize=(4.1,2))
        fig.subplots_adjust(left=0.15, bottom=0.22, right=0.98, top=0.87)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)

        opocoef = -coef
        ax.set_title(r'$\times$'+f'10$^{{{-coef}}}$'+varunit[ivar],loc='left', fontsize=13, pad=1)

        x = df.index
        y = df[ob].values

        ind = ~np.isnan(y)
        xs = x[ind]
        ys = y[ind]

        X = sm.add_constant(xs)
        model = sm.OLS(ys,X).fit()

        X = sm.add_constant(x)
        pred = model.get_prediction(X)
        ci = pred.conf_int()

        ax.plot(x,ci[:,0], color='gray', linestyle='none', marker='.', markersize=2)
        ax.plot(x,ci[:,1], color='gray', linestyle='none', marker='.', markersize=2)
        ax.fill_between(x, ci[:,0], ci[:,1], color='#E0E0E0')

        ax.plot(x,y, color='k', linestyle='-', linewidth=3)
        ax.plot(x,y, color='w', linestyle='-', linewidth=0.5)

        slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)
        yfit = years*slope + intercept
        ax.plot(years, yfit, color='k', linestyle='--', linewidth=2)

        res = mk.original_test(y)
        pvalue = res.p

        if pvalue < 0.01:
            pval = '<0.01'
        elif pvalue < 0.05:
            pval = '<0.05'
        elif pvalue < 0.10:
            pval = '<0.10'
        else:
            pval = f'={pvalue:.2f}'
        ax.set_title(f'{slope*10:+.2f}/dec, p{pval:s}', loc='right', fontsize=14, pad=2)

        ax.set_xticks(np.arange(1980,2030,10))
        ax.set_xticks(np.arange(1980,2030,2), minor=True)
        ax.tick_params(labelsize=13)
        ax.set_xlim([yrbeg,yrend])

        ax.yaxis.set_major_formatter(ticker.FormatStrFormatter("%.1f"))

        ax.set_xlabel('Year', fontsize=15, labelpad=1)
        ax.set_ylabel(varphy[ivar], fontsize=15)

        ymin,ymax = ax.get_ylim()
        ylen = ymax - ymin

        ax.set_ylim([ymin,ymax+0.1*ylen])

        fig.savefig('dgpi_area_wgt_term_ts.'+varnm+'_'+ob.lower()+'1.png', dpi=600)
        plt.show()