#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  9 10:09:05 2018

@author: krajc
"""
# Praca s geodataframes: 
# https://automating-gis-processes.github.io/2016/Lesson1-Intro-Python-GIS.html

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import os

spcs = ['PM10','PM2.5','NOx','SO2','bap']

inpdir = "/home/krajc/Male_zdroje/New_method/noutputs2015/"
outdir = inpdir + "Pictures"
shapeoutdir = inpdir + "Shapes"

# Create outdir if it does not exist:
if not os.path.exists(outdir):
    os.makedirs(outdir)

shapefile = "/home/krajc/ZSJ_obyv/ZSJ_obyv.shp"
shape = gpd.read_file(shapefile, encoding='utf-8')
shape['ID_ZSJ']=shape['ID_ZSJ'].astype('int')

# Nechcene stlpce vo vyslednom zmergovanom subore:
nechcene = ['cat', 'NAZ_ZSJ','ZSJ_STZUJ', 'AREA', 'PERIMETER', 'area_km2', 'hus_int', 
            'ZSJ','ZSJ_x', 'ZSJ_y']


# Tu sa zacne cyklus cez polutanty

#spc = spcs[0]

for spc in spcs:

    outfile = outdir + "/emissions-" + spc + ".png"
    
    inp_fh = inpdir + spc + "-fh.dat"
    inp_nfh = inpdir + spc + "-nfh.dat"
    
    fh = pd.read_csv(inp_fh, sep='|' )
    nfh = pd.read_csv(inp_nfh, sep='|' )
    
    tmp = shape.merge(fh,'left', left_on='ID_ZSJ',right_on='ZSJ')
    
    # Kontrola
    #for i in fh['ZSJ'].unique():
    #   if i not in shape['ID_ZSJ'].unique():
    #        print(i)
            
    emissions = tmp.merge(nfh,'left', left_on='ID_ZSJ',right_on='ZSJ')
        
    emissions['Emissions'] =emissions['ETOTAL_x'] + emissions['ETOTAL_y']
    
    # Remove unwanted columns:
    
    for item in nechcene:
        del emissions[item]
    
    # Export to shape:
    outshape =  shapeoutdir + "/emissions-" + spc + ".shp"
    # Create outdir if it does not exist:
    if not os.path.exists(shapeoutdir):
        os.makedirs(shapeoutdir)
        
    emissions.to_file(outshape)

## Vykreslovanie

# Premenna
param = 'Emissions'

# Hranice premennej
Emin, Emax = min(emissions[param]), max(emissions[param])

# create figure and axes for Matplotlib
fig, ax = plt.subplots(1, figsize=(15, 8))

# Map
emissions.plot(column=param, cmap='Reds', linewidth=0.8, ax=ax, edgecolor='0.8')

# Ak chcem odstranit os:
ax.axis('off')

# add a title
mytitle = "Emisie " + spc + " z lokálnych kúrenísk (kg/rok)"
ax.set_title(mytitle, fontdict={'fontsize': '25', 'fontweight' : '3'})

# create an anotation
ax.annotate('Zdroj: SHMÚ', xy=(0.1, .08), xycoords='figure fraction', horizontalalignment='left',
            verticalalignment='top', fontsize=12)

# Create colorbar as a legend
sm = plt.cm.ScalarMappable(cmap='Reds', norm=plt.Normalize(vmin=Emin, vmax=Emax))

# empty array for the data range
sm._A = []
# add the colorbar to the figure
cbar = fig.colorbar(sm)

# Export figure to file
fig.savefig(outfile, dpi=300)