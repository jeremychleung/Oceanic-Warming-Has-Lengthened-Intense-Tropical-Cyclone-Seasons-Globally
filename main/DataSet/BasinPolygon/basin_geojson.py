# -*- coding: utf-8 -*-
"""
Created on Fri Sep 20 13:06:46 2024

@author: Jimmy Liu, UCAS&LZU
"""

import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon

oceanbasin = ['NA','EP','WP','SI','SP']
nbasin = len(oceanbasin)

geobasin = {}

polygons = []

for iob,ob in enumerate(oceanbasin):
    for pp in range(2):
        match (ob,pp):
            case ('NA',0):
                lat = [25,10,10,25,25]
                lon = [258.5,275,330,330,258.5]
            case ('EP',0):
                lat = [20,8,8,20,20]
                lon = [230,230,276.7,264,230]
            case ('WP',0):
                lat = [15,5,5,15,15]
                lon = [120,120,170,170,120]
            case ('SI',0):
                lat = [-5,-15,-15,-5,-5]
                lon = [50,50,115,115,50]
            case ('SP',0):
                lat = [-8,-18,-18,-8,-8]
                lon = [145,145,195,195,145]

            case ('NA',1):
                lat = [25,10,10,25,25]
                lon = [258.5,275,330,330,258.5]
            case ('EP',1):
                lat = [18,8,8,18,18]
                lon = [220,220,276.9,266,220]
            case ('WP',1):
                lat = [18,8,8,18,18]
                lon = [130,130,180,180,130]
            case ('SI',1):
                lat = [-5,-15,-15,-5,-5]
                lon = [50,50,115,115,50]
            case ('SP',1):
                lat = [-8,-18,-18,-8,-8]
                lon = [145,145,195,195,145]

        geobasin[f'{ob:2s}{pp:1d}'] = {'lat':lat, 'lon':lon}

        points = list(zip(lon,lat))
        polygons.append(Polygon(points))

#%%
np.save('basin.npy', geobasin)

basins = [f'{x}{y:1d}' for x in oceanbasin for y in [0,1]]
gdf = gpd.GeoDataFrame({'basin':basins, 'geometry':polygons}, crs="EPSG:4326")
gdf.to_file('basin.geojson', driver='GeoJSON', crs=None, encoding='utf-8')