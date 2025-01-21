# -*- coding: utf-8 -*-
"""
Created on Tue Dec 17 21:36:00 2024

@author: Jimmy Liu, UCAS&LZU
"""

import json
import cmaps
import numpy as np
import geopandas as gpd
import pymannkendall as mk
from scipy import stats
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap,shiftgrid
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
gdf = gpd.read_file('../DataSet/BasinPolygon/basin.geojson')

u200 = np.load('./data/u200.npy', allow_pickle=True)
v200 = np.load('./data/v200.npy', allow_pickle=True)

lats = v200.item()['lat']
lons = v200.item()['lon']
years = v200.item()['year']

ny = lats.size
nx = lons.size
nyear = years.size

X,Y = np.meshgrid(lons,lats)

#%%
oceanbasin = ['NA','WP']
nbasin = len(oceanbasin)

for iob,ob in enumerate(oceanbasin):
    u = u200.item()[ob.lower()+'1']
    v = v200.item()[ob.lower()+'1']
    u = np.array(u)
    v = np.array(v)

    uv = np.sqrt(u**2 + v**2)
    um = np.nanmean(u, axis=0)
    vm = np.nanmean(v, axis=0)

    trend = np.full([ny,nx], fill_value=np.nan)
    ptest = np.full([ny,nx], fill_value=np.nan)
    for iy,ilat in enumerate(lats):
        for ix,ilon in enumerate(lons):
            x = years
            y = uv[:,iy,ix]

            ind = ~np.isnan(y)
            xs = x[ind]
            ys = y[ind]

            slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)
            res = mk.original_test(y)
            pvalue = res.p

            trend[iy,ix] = slope*10
            ptest[iy,ix] = pvalue

    #--------------------------------------
    if ob == 'NA':
        lon0,lat0 = -58,20
    elif ob == 'WP':
        lon0,lat0 = 150,20

    #basin polygon
    polygon = gdf[gdf['basin'] == f'{ob:2s}1']
    polygon = polygon['geometry'].to_json()
    polygon_dict = json.loads(polygon)
    lonlat = polygon_dict['features'][0]['geometry']['coordinates'][0]
    lonlat = np.array(lonlat)

    fig,ax = plt.subplots(1,1,figsize=(1.6,1.6))
    fig.subplots_adjust(left=0.02, bottom=0.02, right=0.98, top=0.98)

    h = 3000.0
    m = Basemap(projection='nsper', lon_0=lon0,lat_0=lat0, satellite_height=h*1000.0, resolution='l',ax=ax)
    m.fillcontinents(color='#B2B3B7',lake_color='w')
    m.drawcoastlines(color='gray', linewidth=0.5)
    m.drawparallels(np.arange(-90,90.1,30),labels=[0,0,0,0],linewidth=0.5,linestyle='--',color='k',fontsize=10)
    m.drawmeridians(np.arange(0,360.1,30),labels=[0,0,0,0],linewidth=0.5,linestyle='--',color='k',fontsize=10)
    #m.drawmapboundary(fill_color='aqua')

    mX,mY = m(X,Y)

    cint = np.arange(-2.0,2.01,0.2)
    cf = m.contourf(mX,mY,trend, levels=cint, cmap=cmaps.testcmap, extend='both')

    ugrid,newlons = shiftgrid(180,um,lons,start=False)
    vgrid,newlons = shiftgrid(180,vm,lons,start=False)
    uproj,vproj,xx,yy = m.transform_vector(ugrid,vgrid,newlons,lats,30,30,returnxy=True,masked=True)
    Q = m.quiver(xx,yy,uproj,vproj,scale=200, width=0.004)
    qk = plt.quiverkey(Q, 0.08, 0.08, 20, '20m/s',labelpos='S',labelsep=0.04,fontproperties={'size':8})

    m.contourf(mX,mY,ptest,levels=[0,0.05],colors='none',hatches=['xxxxx'])

    nline = lonlat.shape[0]
    for i in range(nline-1):
        xx0 = lonlat[i,0]; yy0 = lonlat[i,1]
        xx1 = lonlat[i+1,0]; yy1 = lonlat[i+1,1]
        if (xx0!=xx1) and (yy0!=yy1):
            xx = np.linspace(xx0,xx1,num=1000)
            yy = np.linspace(yy0,yy1,num=1000)
        elif xx0==xx1:
            yy = np.linspace(yy0,yy1,num=1000)
            xx = np.full_like(yy, fill_value=xx0)
        elif yy0==yy1:
            xx = np.linspace(xx0,xx1,num=1000)
            yy = np.full_like(xx, fill_value=yy0)
        m.plot(xx,yy,color='k', linewidth=1.5,latlon=True)

    print(ob, np.nanmin(trend), np.nanmax(trend))
    fig.savefig('uv200_reg_near.'+f'{ob.lower()}1'+'.png', dpi=600)
    plt.show()

    plt.quiver(X,Y,um,vm, scale=1, scale_units='xy', angles='xy')
    if ob == 'NA':
        plt.xlim([260,360])
    elif ob == 'WP':
        plt.xlim([100,180])
    plt.ylim([0,50])