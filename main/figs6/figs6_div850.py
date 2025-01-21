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

u850 = np.load('../figs5/data/u850.npy', allow_pickle=True)
v850 = np.load('../figs5/data/v850.npy', allow_pickle=True)
div850 = np.load('../figs5/data/div850.npy', allow_pickle=True)

lats = div850.item()['lat']
lons = div850.item()['lon']
years = div850.item()['year']

ny = lats.size
nx = lons.size
nyear = years.size

X,Y = np.meshgrid(lons,lats)

#%%
oceanbasin = ['WP']
nbasin = len(oceanbasin)

for iob,ob in enumerate(oceanbasin):
    u = u850.item()[ob.lower()+'1']
    v = v850.item()[ob.lower()+'1']
    div = div850.item()[ob.lower()+'1']
    u = np.array(u)
    v = np.array(v)
    div = np.array(div)

    uv = np.sqrt(u**2 + v**2)

    um = np.nanmean(u, axis=0)
    vm = np.nanmean(v, axis=0)
    divm = np.nanmean(div, axis=0)

    #--------------------------------------------
    uvtrend = np.full([ny,nx], fill_value=np.nan)
    uvptest = np.full([ny,nx], fill_value=np.nan)
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

            uvtrend[iy,ix] = slope*10
            uvptest[iy,ix] = pvalue

    #--------------------------------------------
    trend = np.full([ny,nx], fill_value=np.nan)
    ptest = np.full([ny,nx], fill_value=np.nan)
    for iy,ilat in enumerate(lats):
        for ix,ilon in enumerate(lons):
            x = years
            y = div[:,iy,ix]

            ind = ~np.isnan(y)
            if np.sum(ind)<20: continue
            xs = x[ind]
            ys = y[ind]

            slope, intercept, rvalue, pvalue, std_err = stats.linregress(xs,ys)
            res = mk.original_test(y)
            pvalue = res.p

            trend[iy,ix] = slope*10
            ptest[iy,ix] = pvalue

    divm *= 1e6
    trend *= 1e6

    print(ob, np.nanmin(trend), np.nanmax(trend))

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

    cint = np.arange(-1.0,1.01,0.1)
    cf = m.contourf(mX,mY,trend, levels=cint, cmap=cmaps.testcmap, extend='both')

    ugrid,newlons = shiftgrid(180,um,lons,start=False)
    vgrid,newlons = shiftgrid(180,vm,lons,start=False)
    uproj,vproj,xx,yy = m.transform_vector(ugrid,vgrid,newlons,lats,30,30,returnxy=True,masked=True)
    Q = m.quiver(xx,yy,uproj,vproj,scale=100, width=0.004)
    qk = plt.quiverkey(Q, 0.08, 0.08, 10, '10m/s',labelpos='S',labelsep=0.04,fontproperties={'size':7})

    m.contourf(mX,mY,ptest,levels=[0,0.05],colors='none',hatches=['xxxxx'])

    um[uvptest>0.10] = np.nan
    vm[uvptest>0.10] = np.nan
    uvtrend[uvptest>0.10] = np.nan
    ugrid2,newlons = shiftgrid(180,um,lons,start=False)
    vgrid2,newlons = shiftgrid(180,vm,lons,start=False)
    uvtrend2,newlons = shiftgrid(180,uvtrend,lons,start=False)
    uproj2,vproj2,xxproj,yyproj = m.transform_vector(ugrid2,vgrid2,newlons,lats,30,30,returnxy=True,masked=True)
    uvtrend_proj,xxproj,yyproj = m.transform_scalar(uvtrend2, newlons, lats, 30,30,returnxy=True,masked=True)

    uproj2_neg = uproj2.copy()
    vproj2_neg = vproj2.copy()
    uproj2_neg[uvtrend_proj>0] = np.nan
    vproj2_neg[uvtrend_proj>0] = np.nan

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
        m.plot(xx,yy,color='k', linewidth=1.5,latlon=True, zorder=1)

    Q = m.quiver(xxproj,yyproj,uproj2,vproj2, scale=100, width=0.01, color='r', zorder=2)
    Q = m.quiver(xxproj,yyproj,uproj2_neg,vproj2_neg, scale=100, width=0.01, color='deepskyblue', zorder=2)

    #---------------------------------------------------------------
    fig.savefig('div850_reg_near.'+f'{ob.lower()}1'+'.png', dpi=600)
    plt.show()

#%%
fig,ax = plt.subplots(1,1,figsize=(3.8,3.8))
fig.subplots_adjust(left=0.05, bottom=0.30, right=0.95, top=0.98)

h = 3000.0
m = Basemap(projection='nsper', lon_0=lon0,lat_0=lat0, satellite_height=h*1000.0, resolution='l',ax=ax)

m.drawcoastlines(color='gray', linewidth=.5)
m.drawparallels(np.arange(-90,91,30),labels=[0,0,0,0], linewidth=0.5,linestyle='--',color='k',fontsize=10)
m.drawmeridians(np.arange(0,361,30),labels=[0,0,0,0], linewidth=0.5,linestyle='--',color='k',fontsize=10)
#m.drawmapboundary(fill_color='aqua')

mX,mY = m(X,Y)

cint = np.arange(-1.0,1.01,0.1)
cf=m.contourf(mX,mY,trend, levels=cint, cmap=cmaps.testcmap, extend='both')
m.contourf(mX,mY,ptest,levels=[0,0.05],colors='none',hatches=['xxxx'])
m.fillcontinents(color='#B2B3B7',lake_color='w')
m.plot(lonlat[:,0],lonlat[:,1],color='k', linewidth=2)

#--------------------------------
axleft = ax.get_position().x0
axright = ax.get_position().x1
axc = (axleft + axright)/2

y0 = ax.get_position().y0

cbwidth = 0.95
cbheight = 0.04
dd = 0.07

cax = fig.add_axes([axc-cbwidth/2,y0-dd,cbwidth,cbheight])
cb = fig.colorbar(cf, cax=cax, orientation='horizontal')

cb.ax.set_xticks(cint[::2])
cb.ax.set_xticklabels([f'{x:.1f}' if abs(x)>0.1 else '0' for x in cb.ax.get_xticks()])
cb.ax.tick_params(labelsize=11, top=False,labeltop=False, bottom=True,labelbottom=True, pad=1.8)
cb.ax.set_xlabel(r'Trend [$\times10^{-6}$'+'m s'+r'$^{-2}$/dec]', fontsize=11, labelpad=1)

fig.savefig('div850_cb.png', dpi=600)