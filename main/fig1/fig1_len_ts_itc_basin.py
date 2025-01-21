# -*- coding: utf-8 -*-
"""
Created on Thu Jun 20 12:39:01 2024

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
rcParams['mathtext.fontset'] = 'stix'
rcParams['mathtext.default'] = 'regular'

#%%
Ndts = pd.date_range('20220216','20230215',freq='D')
Sdts = pd.date_range('20220816','20230815',freq='D')
N1st = np.argwhere(Ndts.day==1).ravel()
S1st = np.argwhere(Sdts.day==1).ravel()
Nlab = ['Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec','Jan','Feb']
Slab = ['Sep','Oct','Nov','Dec','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug']

#%%
yrsrt = 1980
yrend = 2023
years = np.arange(yrsrt,yrend+1)
nyear = years.size

ibtdf = pd.read_csv('../DataSet/ibtracs_lmi_time_leapyear.csv', index_col='sid', keep_default_na=False)

#%%
oceanbasin = ['NA','EP','WP','SI','SP']
n_basin = len(oceanbasin)

fig,axs = plt.subplots(1,5,figsize=(10,1.7), sharex=True)
fig.subplots_adjust(left=0.05, bottom=0.20, right=0.99, top=0.83, wspace=0.18, hspace=0.35)

for iob,ob in enumerate(oceanbasin):
    ax = axs[iob]
    ax.spines[:].set_linewidth(1.2)
    #print(iob,ob)

    #--------------------------------------------------------------------------
    x0 = ax.get_position().x0
    x1 = ax.get_position().x1
    y0 = ax.get_position().y0
    y1 = ax.get_position().y1
    xw = x1 - x0
    yw = y1 - y0

    if ob == 'NH':
        cond1 = ibtdf['basin'].isin(['NA','EP','WP'])
    elif ob == 'SH':
        cond1 = ibtdf['basin'].isin(['SI','SP'])
    else:
        cond1 = ibtdf['basin'] == ob

    #--------------------------------------------------------------------------
    TSyr = np.full([nyear,3], fill_value=np.nan)
    ITCyr = np.full([nyear,3], fill_value=np.nan)

    cond2 = ibtdf['sshs'] >= 0
    for iyr,yr in enumerate(years):
        cond3 = (ibtdf['season'] >= yr-1) & (ibtdf['season'] <= yr+1)
        cond = cond1 & cond2 & cond3

        if ibtdf[cond].shape[0] == 0: continue
        TSyr[iyr,0] = np.percentile(ibtdf[cond]['occurtime'].values, 5)
        TSyr[iyr,1] = np.percentile(ibtdf[cond]['occurtime'].values, 95)
        TSyr[iyr,2] = TSyr[iyr,1] - TSyr[iyr,0]

    cond2 = ibtdf['sshs'] >= 4
    for iyr,yr in enumerate(years):
        cond3 = (ibtdf['season'] >= yr-1) & (ibtdf['season'] <= yr+1)
        cond = cond1 & cond2 & cond3

        if ibtdf[cond].shape[0] == 0: continue
        ITCyr[iyr,0] = np.percentile(ibtdf[cond]['occurtime'].values, 5)
        ITCyr[iyr,1] = np.percentile(ibtdf[cond]['occurtime'].values, 95)
        ITCyr[iyr,2] = ITCyr[iyr,1] - ITCyr[iyr,0]

    TSdf = pd.DataFrame(TSyr, index=years, columns=['beg','end','len'])
    ITCdf = pd.DataFrame(ITCyr, index=years, columns=['beg','end','len'])

    #%%--------------------------------------------------------------------------
    #TS season length
    x = years
    y = TSdf['len'].values
    ind = ~np.isnan(y)
    xs = x[ind]
    ys = y[ind]

    X = sm.add_constant(xs)
    model = sm.OLS(ys,X).fit()

    X = sm.add_constant(x)
    pred = model.get_prediction(X)
    ci = pred.conf_int()

    ax.plot(x,ci[:,0], linestyle='none', marker='.', markersize=3, color='k', markerfacecolor='k', markeredgewidth=0, alpha=0.6)
    ax.plot(x,ci[:,1], linestyle='none', marker='.', markersize=3, color='k', markerfacecolor='k', markeredgewidth=0, alpha=0.6)
    ax.fill_between(x, ci[:,0], ci[:,1], color='k', alpha=0.2)

    ax.plot(x,y, color='k', linestyle='-', linewidth=3)

    slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)
    res = mk.original_test(y)
    pvalue = res.p

    yfit = years*slope + intercept
    ax.plot(years, yfit, color='k', linestyle='--', linewidth=2)

    if pvalue < 0.01:
        pval = '<0.01'
    elif pvalue < 0.05:
        pval = '<0.05'
    elif pvalue < 0.10:
        pval = '<0.10'
    else:
        pval = f'={pvalue:.2f}'
    ax.text(0.00,1.15,f'{slope*10:+.2f}d/dec, p{pval:s}', color='k', fontdict={'weight':'bold','size':9}, transform=ax.transAxes)

    #%%------------------------------------------------------------------------
    #ITC season length
    x = years
    y = ITCdf['len'].values
    ind = ~np.isnan(y)
    xs = x[ind]
    ys = y[ind]

    X = sm.add_constant(xs)
    model = sm.OLS(ys,X).fit()

    X = sm.add_constant(x)
    pred = model.get_prediction(X)
    ci = pred.conf_int()

    ax.plot(x,ci[:,0], linestyle='none', marker='.', markersize=3, color='r', markerfacecolor='r', markeredgewidth=0, alpha=0.6)
    ax.plot(x,ci[:,1], linestyle='none', marker='.', markersize=3, color='r', markerfacecolor='r', markeredgewidth=0, alpha=0.6)
    ax.fill_between(x, ci[:,0], ci[:,1], color='r', alpha=0.2)

    ax.plot(x,y, color='r', linestyle='-', linewidth=3)

    slope, intercept, rvalue, pvalue1, std_err = stats.linregress(xs,ys)
    res = mk.original_test(y)
    pvalue = res.p

    yfit = years*slope + intercept
    ax.plot(years, yfit, color='r', linestyle='--', linewidth=2)

    if pvalue < 0.01:
        pval = '<0.01'
    elif pvalue < 0.05:
        pval = '<0.05'
    elif pvalue < 0.10:
        pval = '<0.10'
    else:
        pval = f'={pvalue:.2f}'
    ax.text(0.00,1.03,f'{slope*10:+.2f}d/dec, p{pval:s}', color='r', fontdict={'weight':'bold','size':9}, transform=ax.transAxes)

    len_ratio = slope/np.mean(ys)*100
    print(f'{ob:2s}: mean length:{np.nanmean(ys):5.1f}d, slope:{slope*10:4.1f}d, relative change:{len_ratio*10:4.1f}%')
    print(f'    t-test:{pvalue1:.3f}, mk-test:{pvalue:.3f}\n')

    #-----------------------
    txtob = ob
    if ob == 'EP':
        txtob = 'ENP'
    elif ob == 'WP':
        txtob = 'WNP'
    ax.set_title(txtob, loc='right', fontdict={'weight':'normal','size':12}, pad=3)

    ax.set_xticks(np.arange(1980,2030,10))
    ax.set_xticks(np.arange(1980,2030,2), minor=True)
    ax.tick_params(labelsize=8.5, pad=2)
    ax.set_xlim([yrsrt,yrend])

    ax.set_xlabel('Year', fontsize=12, labelpad=1)
    if ob in ['NA']:
        ax.set_ylabel('Season Length [day]', fontsize=12, labelpad=2)

    ax.text(-0.13,1.04,chr(iob+102), fontdict={'weight':'bold','size':19}, transform=ax.transAxes)

#%%%---------------------------------------------------------------------------
plt.show()
fig.savefig('fig1_len_ts_itc_basin.png', dpi=600)
plt.close()