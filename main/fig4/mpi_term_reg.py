# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 16:05:40 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pymannkendall as mk
from scipy import stats

#%%
sstdata = np.load('../DGPI/sst.npy', allow_pickle=True)
mpidata = np.load('../MPI/mpi_data.npy', allow_pickle=True)

years = mpidata.item()['year']
lat = mpidata.item()['lat']
lon = mpidata.item()['lon']

yrbeg = years[0]
yrend = years[-1]
nyear = years.size

ny = lat.size
nx = lon.size

#%%
CKCD = 0.9
VREDUC = 0.8

oceanbasin = ['NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

regdict = dict()
regdict['lat'] = lat
regdict['lon'] = lon
regdict['year'] = years
for iob,ob in enumerate(oceanbasin):
    for pp in [0,1]:
        print(f'{ob:2s} {pp:1d}')

        sst = sstdata.item()[ob.lower()+f'{pp:1d}']
        sst = np.array(sst).transpose(2,1,0)

        mpi = mpidata.item()[ob.lower()+f'{pp:1d}']['vmax']
        rat = mpidata.item()[ob.lower()+f'{pp:1d}']['rat']
        ksk = mpidata.item()[ob.lower()+f'{pp:1d}']['fac']

        mpi_bar = np.nanmean(mpi,axis=2)
        rat_bar = np.nanmean(rat,axis=2)
        ksk_bar = np.nanmean(ksk,axis=2)

        const = np.full([ny,nx], fill_value=np.nan)
        for ix in range(nx):
            for iy in range(ny):
                if np.isnan(mpi_bar[iy,ix]): continue
                if mpi_bar[iy,ix]<1: continue
                const[iy,ix] = VREDUC**2*CKCD/(2*mpi_bar[iy,ix])

        #---------------------------------------------
        mpi_s = np.full([ny,nx], fill_value=np.nan)
        mpi_p = np.full_like(mpi_s, fill_value=np.nan)

        for ix in range(nx):
            for iy in range(ny):
                x = years
                y = mpi[iy,ix,:]
                ind = ~np.isnan(y)
                if np.sum(ind)<30: continue
                xs = x[ind]
                ys = y[ind]

                slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)
                res = mk.original_test(y)
                pvalue = res.p
                mpi_s[iy,ix] = slope*10
                mpi_p[iy,ix] = pvalue

        #---------------------------------------------
        rat_s = np.full([ny,nx], fill_value=np.nan)
        rat_p = np.full_like(rat_s, fill_value=np.nan)

        for ix in range(nx):
            for iy in range(ny):
                x = years
                y = rat[iy,ix,:]
                ind = ~np.isnan(y)
                if np.sum(ind)<30: continue
                xs = x[ind]
                ys = y[ind]

                slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)
                res = mk.original_test(y)
                pvalue = res.p
                rat_s[iy,ix] = slope*10
                rat_p[iy,ix] = pvalue

        #---------------------------------------------
        ksk_s = np.full([ny,nx], fill_value=np.nan)
        ksk_p = np.full_like(ksk_s, fill_value=np.nan)

        for ix in range(nx):
            for iy in range(ny):
                x = years
                y = ksk[iy,ix,:]
                ind = ~np.isnan(y)
                if np.sum(ind)<30: continue
                xs = x[ind]
                ys = y[ind]

                slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)
                res = mk.original_test(y)
                pvalue = res.p
                ksk_s[iy,ix] = slope*10
                ksk_p[iy,ix] = pvalue

        #----------------------------------------------
        ksk_term = const*rat_bar*ksk_s
        rat_term = const*ksk_bar*rat_s

        right = ksk_term + rat_term
        right_p = np.full_like(right, fill_value=np.nan)

        regdict[ob.lower()+f'{pp:1d}'] = {'slope':{'mpi':mpi_s,'tol':right, 'rat':rat_term, 'ksk':ksk_term},
                                          'p':{'mpi':mpi_p, 'tol':right_p, 'rat':rat_p, 'ksk':ksk_p}}

#-------------------------------
np.save('mpi_term_reg', regdict)