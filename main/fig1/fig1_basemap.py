# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 20:43:50 2024

@author: Jimmy Liu, UCAS&LZU
"""

from matplotlib import pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib import rcParams

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
fig,ax = plt.subplots(1,1,figsize=(4,1.2))
fig.subplots_adjust(left=0.03, bottom=0.01, right=0.99, top=0.99)

ax.spines[:].set_linewidth(0.3)

m = Basemap(projection='cyl', lat_0=0, lon_0=195, resolution='l', ax=ax)
#m.drawmapboundary(fill_color='lightblue')
#m.shadedrelief(scale=0.8)
m.fillcontinents(color='#B2B3B7',lake_color='w')
m.drawmapboundary(fill_color='w')
m.drawcoastlines(color='gray', linewidth=.25)
#ax.set_xticks(np.arange(0,361,90))
#ax.set_xticks(np.arange(0,361,30), minor=True)
#ax.set_yticks(np.arange(-90,90.1,30))
#ax.set_xticklabels(labels=[r'$0\degree$',r'$90\degree$E',r'$180\degree$',r'$90\degree$W',r'$0\degree$'])
#ax.set_yticklabels(labels=[r'$90\degree$S',r'$60\degree$S',r'$30\degree$S',r'$0\degree$',r'$30\degree$N',r'$60\degree$N',r'$90\degree$N'])
ax.tick_params(which='both', left=False, right=False, top=False, bottom=False,
               labelbottom=False, labelleft=False, labelsize=7, pad=2)

lw = 0.8
lc = 'k'
m.plot([ 20,360],[ 0,  0], latlon=True, linewidth=lw, color=lc)
m.plot([360,360],[ 0, 90], latlon=True, linewidth=lw, color=lc)
m.plot([100,100],[ 0, 90], latlon=True, linewidth=lw, color=lc)
m.plot([180,180],[ 0, 90], latlon=True, linewidth=lw, color=lc)
m.plot([260,260],[20, 90], latlon=True, linewidth=lw, color=lc)
m.plot([260,284],[20,  7], latlon=True, linewidth=lw, color=lc)
m.plot([284,284],[ 0,  7], latlon=True, linewidth=lw, color=lc)
m.plot([ 20, 20],[ 0,-90], latlon=True, linewidth=lw, color=lc)
m.plot([135,135],[ 0,-90], latlon=True, linewidth=lw, color=lc)
m.plot([240,240],[ 0,-90], latlon=True, linewidth=lw, color=lc)

#----------------------------------------
ax.text(0.82,0.88,'NA', fontdict={'weight':'normal','size':5}, transform=ax.transAxes)
ax.text(0.54,0.88,'ENP', fontdict={'weight':'normal','size':5}, transform=ax.transAxes)
ax.text(0.36,0.88,'WNP', fontdict={'weight':'normal','size':5}, transform=ax.transAxes)
ax.text(0.170,0.075,'SI', fontdict={'weight':'normal','size':5}, transform=ax.transAxes)
ax.text(0.450,0.075,'SP', fontdict={'weight':'normal','size':5}, transform=ax.transAxes)

#----------------------------------------
#legend
lgx0 = 0.71; w = 0.03
ax.fill([lgx0,lgx0+w,lgx0+w,lgx0],[0.36,0.36,0.39,0.39], color='b',  transform=ax.transAxes, zorder=2)
ax.fill([lgx0,lgx0+w,lgx0+w,lgx0],[0.26,0.26,0.29,0.29], color='r',  transform=ax.transAxes, zorder=2)
ax.fill([lgx0,lgx0+w,lgx0+w,lgx0],[0.16,0.16,0.19,0.19], color='gray',  transform=ax.transAxes, zorder=2)
ax.fill([lgx0,lgx0+w,lgx0+w,lgx0],[0.06,0.06,0.09,0.09], color='k',  transform=ax.transAxes, zorder=2)

ax.text(lgx0+0.04,0.355, 'Intense TC Season (1980-2001)', fontsize=4.5, transform=ax.transAxes, zorder=2)
ax.text(lgx0+0.04,0.255, 'Intense TC Season (2002-2023)', fontsize=4.5, transform=ax.transAxes, zorder=2)
ax.text(lgx0+0.04,0.155, 'Overall TC Season (1980-2001)', fontsize=4.5, transform=ax.transAxes, zorder=2)
ax.text(lgx0+0.04,0.055, 'Overall TC Season (2002-2023)', fontsize=4.5, transform=ax.transAxes, zorder=2)

ax.set_ylim([-50,55])

#%%
fig.savefig('fig1_basemap.png', dpi=550)