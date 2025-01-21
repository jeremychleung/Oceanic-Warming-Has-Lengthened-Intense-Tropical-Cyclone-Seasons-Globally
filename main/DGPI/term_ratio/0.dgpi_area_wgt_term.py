# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 08:50:08 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

#%%
dgpidata = np.load('../dgpi_data.npy', allow_pickle=True)
gdf = gpd.read_file('../../DataSet/BasinPolygon/basin.geojson')

years = dgpidata.item()['year']
lat = dgpidata.item()['lat']
lon = dgpidata.item()['lon']

nyear = years.size
ny = lat.size
nx = lon.size
X,Y = np.meshgrid(lon,lat)

#%%
wgt = np.full([ny,nx], fill_value=np.nan)
for iy,ilat in enumerate(lat):
    wgt[iy,:] = np.cos(np.deg2rad(ilat))

oceanbasin = ['NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

varlist = ['aa','bb','cc','dd','dgpi','a','b','c','d','bcd','acd','abd','abc']

for var in varlist:
    index_mean = np.full([nbasin,2,nyear], fill_value=np.nan)
    for iob,ob in enumerate(oceanbasin):
        print(var,ob)
        for pp in range(2):
            polygon = gdf[gdf['basin'] == f'{ob:2s}{pp:1d}']

            mask = np.full([ny,nx], fill_value=False, dtype=bool)
            for iy,ilat in enumerate(lat):
                for ix,ilon in enumerate(lon):
                    point = Point(ilon,ilat)
                    mask[iy,ix] = polygon['geometry'].contains(point).values

            #-------------------------------------------------
            data = dgpidata.item()[ob.lower()+f'{pp:1d}'][var]

            for iyr,yr in enumerate(years):
                data_yr = data[iyr,:,:]
                mask_yr = mask & ~np.isnan(data_yr)

                if mask_yr.any():
                    w = wgt[mask_yr]
                    wsum = w.sum()

                    m = data_yr[mask_yr]
                    index_mean[iob,pp,iyr] = np.nansum(w*m)/wsum

    #-------------------------------------------
    for pp in [0,1]:
        index_avg = pd.DataFrame(data=index_mean[:,pp,:].T, index=years, columns=oceanbasin)
        index_avg.to_csv(var+'_area_wgt'+str(pp)+'.csv', index=True)