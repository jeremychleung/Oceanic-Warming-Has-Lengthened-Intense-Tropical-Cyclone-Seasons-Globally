# -*- coding: utf-8 -*-
"""
Created on Wed Dec 11 19:18:48 2024

@author: Jimmy Liu, UCAS&LZU
"""

import json
import cmaps
import numpy as np
import geopandas as gpd
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from shapely.geometry import Point,Polygon
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = 'Helvetica'
rcParams['xtick.top'] = 'False'
rcParams['ytick.right'] = 'False'
rcParams['xtick.direction'] = 'out'
rcParams['ytick.direction'] = 'out'
rcParams['hatch.color'] = 'k'
rcParams['hatch.linewidth'] = 0.6
#rcParams['mathtext.fontset'] = 'stix'
rcParams['mathtext.fontset'] = 'custom'
rcParams['mathtext.fallback'] = 'stix'
rcParams['mathtext.default'] = 'regular'

#%%
regdata = np.load('mpi_term_reg.npy', allow_pickle=True)
gdf = gpd.read_file('../DataSet/BasinPolygon/basin.geojson')

years = regdata.item()['year']
lat = regdata.item()['lat']
lon = regdata.item()['lon']

nyear = years.size
ny = lat.size
nx = lon.size
X,Y = np.meshgrid(lon,lat)

#%%
oceanbasin = ['NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

varlist = ['mpi','rat','ksk']
for iob,ob in enumerate(oceanbasin):
    if ob == 'NA':
        lon0,lat0 = -60,20
    elif ob == 'EP':
        lon0,lat0 = -110,15
    elif ob == 'WP':
        lon0,lat0 = 150,10
    elif ob == 'SI':
        lon0,lat0 = 85,-10
    elif ob == 'SP':
        lon0,lat0 = 165,-15

    for pp in [0,1]:
        if (pp==1) and (ob not in ['NA']): continue
        if (pp==0) and (ob not in ['EP','WP','SI','SP']): continue

        #basin polygon
        polygon = gdf[gdf['basin'] == f'{ob:2s}{pp:1d}']
        polygon = polygon['geometry'].to_json()
        polygon_dict = json.loads(polygon)
        lonlat = polygon_dict['features'][0]['geometry']['coordinates'][0]
        lonlat = np.array(lonlat)

        for iv,varnm in enumerate(varlist):
            #if varnm!='ksk': continue
            trend = regdata.item()[ob.lower()+f'{pp:1d}']['slope'][varnm]
            ptest = regdata.item()[ob.lower()+f'{pp:1d}']['p'][varnm]

            fig,ax = plt.subplots(1,1,figsize=(1.6,1.6))
            fig.subplots_adjust(left=0.02, bottom=0.02, right=0.98, top=0.98)

            if ob == 'EP':
                if varnm == 'mpi':
                    txt = r'$\Delta{MPI}/\Delta{t}$'
                elif varnm == 'rat':
                    txt = r'$\Delta{\eta}/\Delta{t}$'
                elif varnm == 'ksk':
                    txt = r'$\Delta{L}/\Delta{t}$'
                #ax.set_title(txt, fontdict={'weight':'bold','size':16}, pad=5)

            h = 3000.0
            m = Basemap(projection='nsper', lon_0=lon0,lat_0=lat0, satellite_height=h*1000.0, resolution='l',ax=ax)

            m.drawcoastlines(color='gray', linewidth=.5)
            m.drawparallels(np.arange(-90,91,30),labels=[0,0,0,0], linewidth=0.5,linestyle='--',color='k',fontsize=10)
            m.drawmeridians(np.arange(0,361,30),labels=[0,0,0,0], linewidth=0.5,linestyle='--',color='k',fontsize=10)

            mX,mY = m(X,Y)

            cint = np.arange(-4,4.2,0.4)
            cf=m.contourf(mX,mY,trend, levels=cint, cmap=cmaps.testcmap, extend='both')
            m.contourf(mX,mY,ptest,levels=[0,0.05],colors='none',hatches=['xxxx'])
            m.fillcontinents(color='#B2B3B7',lake_color='w')
            m.plot(lonlat[:,0],lonlat[:,1],color='k', linewidth=2)

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

            print(ob,pp,varnm, np.nanmin(trend), np.nanmax(trend))
            fig.savefig('mpi_mean_reg_near.'+varnm+'_'+f'{ob.lower()}{pp:1d}'+'.png', dpi=600)
            plt.show()


#%%
fig,ax = plt.subplots(1,1,figsize=(3.8,3.8))
fig.subplots_adjust(left=0.05, bottom=0.12, right=0.95, top=0.98)

h = 3000.0
m = Basemap(projection='nsper', lon_0=lon0,lat_0=lat0, satellite_height=h*1000.0, resolution='l',ax=ax)

m.drawcoastlines(color='gray', linewidth=.5)
m.drawparallels(np.arange(-90,91,30),labels=[0,0,0,0], linewidth=0.5,linestyle='--',color='k',fontsize=10)
m.drawmeridians(np.arange(0,361,30),labels=[0,0,0,0], linewidth=0.5,linestyle='--',color='k',fontsize=10)
#m.drawmapboundary(fill_color='aqua')

mX,mY = m(X,Y)

cint = np.arange(-4,4.2,0.4)
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
dd = 0.05

cax = fig.add_axes([axc-cbwidth/2,y0-dd,cbwidth,cbheight])
cb = fig.colorbar(cf, cax=cax, orientation='horizontal')

cb.ax.set_xticks(cint[::2])
cb.ax.set_xticklabels([f'{x:.1f}' if abs(x)>0.1 else '0' for x in cb.ax.get_xticks()])
cb.ax.tick_params(labelsize=11, top=False,labeltop=False, bottom=True,labelbottom=True, pad=1.8)

fig.savefig('near_cb.png', dpi=600)