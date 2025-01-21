# -*- coding: utf-8 -*-
"""
Created on Sat Dec  7 22:42:24 2024

@author: Jimmy Liu, UCAS&LZU
"""

import json
import cmaps
import numpy as np
import geopandas as gpd
from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
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
regdata = np.load('dgpi_mean_reg.npy', allow_pickle=True)
gdf = gpd.read_file('../DataSet/BasinPolygon/basin.geojson')

years = regdata.item()['year']
lat = regdata.item()['lat']
lon = regdata.item()['lon']

nyear = years.size
ny = lat.size
nx = lon.size
X,Y = np.meshgrid(lon,lat)

#%%
varlist = ['dgpi','a','b','c','d']
varmath = [r'$\Delta{DGPI}/\Delta{t}$', r'$\Delta{V_{s}}/\Delta{t}$', r'$\Delta{U_{y}}/\Delta{t}$',
           r'$\Delta{\omega}/\Delta{t}$', r'$\Delta{\zeta_{a}}/\Delta{t}$']

oceanbasin = ['NA','WP']
nbasin = len(oceanbasin)

for iv,varnm in enumerate(varlist):
    fig,axs = plt.subplots(1,2,figsize=(15.5,4.0))
    fig.subplots_adjust(left=0.06, bottom=0.02, right=0.96, top=0.90, wspace=1.50)

    if varnm == 'dgpi':
        cint = np.arange(-1.1,1.101,0.05)
    else:
        cint = np.arange(-0.7,0.701,0.05)

    for iob,ob in enumerate(oceanbasin):
        ax = axs[iob]

        ax.set_title(varmath[iv], fontdict={'weight':'normal','size':23}, pad=10)
        ax.text(-0.08,0.92,chr(iv*2+iob+97), fontdict={'weight':'bold','size':38}, transform=ax.transAxes)

        #basin polygon
        polygon = gdf[gdf['basin'] == f'{ob:2s}1']
        polygon = polygon['geometry'].to_json()
        polygon_dict = json.loads(polygon)
        lonlat = polygon_dict['features'][0]['geometry']['coordinates'][0]
        lonlat = np.array(lonlat)

        #read data
        trend = regdata.item()[ob.lower()+'1']['slope'][varnm]
        ptest = regdata.item()[ob.lower()+'1']['p'][varnm]
        sst = regdata.item()[ob.lower()+'1']['sst']
        cond = (Y<5) | (Y>35) | (sst<26)
        trend[cond] = np.nan
        ptest[cond] = np.nan

        if ob == 'NA':
            h = 3000.0
            m = Basemap(projection='nsper', lon_0=-58,lat_0=20, satellite_height=h*1000.0, resolution='l',ax=ax)

            m.drawcoastlines(color='gray', linewidth=.5)
            m.drawparallels(np.arange(-90,91,30),labels=[0,0,0,0], linewidth=0.5,linestyle='--',color='k',fontsize=10)
            m.drawmeridians(np.arange(0,361,30),labels=[0,0,0,0], linewidth=0.5,linestyle='--',color='k',fontsize=10)
            #m.drawmapboundary(fill_color='aqua')

            mX,mY = m(X,Y)
            cf=m.contourf(mX,mY,trend,levels=cint, cmap=cmaps.testcmap, extend='both')
            m.contourf(mX,mY,ptest,levels=[0,0.05],colors='none',hatches=['xxx'])
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
        else:
            h = 3000.0
            m = Basemap(projection='nsper', lon_0=150,lat_0=20, satellite_height=h*1000.0, resolution='l',ax=ax)

            m.drawcoastlines(color='gray', linewidth=.5)
            m.drawparallels(np.arange(-90,91,30),labels=[0,0,0,0], linewidth=0.5,linestyle='--',color='k',fontsize=10)
            m.drawmeridians(np.arange(0,361,30),labels=[0,0,0,0], linewidth=0.5,linestyle='--',color='k',fontsize=10)
            #m.drawmapboundary(fill_color='aqua')

            mX,mY = m(X,Y)
            cf = m.contourf(mX,mY,trend,levels=cint, cmap=cmaps.testcmap, extend='both')
            m.contourf(mX,mY,ptest,levels=[0,0.05],colors='none',hatches=['xxx'])
            m.fillcontinents(color='#B2B3B7',lake_color='w')

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

    plt.figtext(0.053,0.65,r'$30\degree$N',fontsize=16)
    plt.figtext(0.070,0.25,r'$0\degree$',fontsize=16)
    plt.figtext(0.697,0.65,r'$30\degree$N',fontsize=16)
    plt.figtext(0.710,0.25,r'$0\degree$',fontsize=16)

    #--------------------------------------------------
    #colorbar
    if varnm in ['dgpi','a','b','c','d']:
        axbot = axs[0].get_position().y0
        axtop = axs[0].get_position().y1
        axc = (axbot + axtop)/2

        x0 = axs[0].get_position().x0

        cbwidth = 0.018
        cbheight = 0.80
        dd = 0.044

        cax = fig.add_axes([x0-dd,axc-cbheight/2,cbwidth,cbheight])
        cb = fig.colorbar(cf, cax=cax, orientation='vertical')
        if varnm == 'dgpi':
            cint = np.arange(-1.1,1.2,0.2)
        else:
            cint = np.arange(-0.7,0.8,0.2)
        cb.ax.set_yticks(cint)
        cb.ax.set_yticklabels([f'{x:.1f}' for x in cb.ax.get_yticks()])
        cb.ax.tick_params(labelsize=17, top=False,left=True, right=False,labeltop=False,labelbottom=True, labelleft=True,labelright=False, pad=1.8)
        #cb.mappable.set_clim([80,100])

    fig.savefig('dgpi_mean_reg_near.'+varnm+'.png', dpi=600)
    plt.show()
    plt.close()