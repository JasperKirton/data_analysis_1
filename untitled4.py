#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 17:45:01 2017

@author: pesa
"""

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import matplotlib  as mpl

import processData1 as data

fig = plt.figure()
ax1 = fig.add_subplot(111, projection='3d')

xp1 = np.arange(len(data.global_multiAns['ways']))

yp1 = np.ones(len(data.global_multiAns['ways']))

xpos = [xp1,xp1,xp1,xp1]
ypos = [yp1,yp1*3,yp1*5,yp1*7]

num_elements = len(xpos)
zpos = np.zeros(len(data.global_multiAns['ways']))
dx = np.ones(len(data.global_multiAns['ways']))
dy = np.ones(len(data.global_multiAns['ways']))

frames = [data.female_multiAns['waysN'],data.male_multiAns['waysN'], 
          data.pnsgen_multiAns['waysN'], data.other_multiAns['waysN']]
          
concat_df = pd.concat(frames)

dz = concat_df


print( data.female_multiAns['waysN'] )

# create all the various bar charts (using 'bottom' attribute to stack them) [normalised]
#ax21.bar(ind-width*1.5-0.01, data.female_multiAns['waysN'], width, color = '#d62728') 
#ax21.bar(ind-width/2-0.01, data.male_multiAns['waysN'], width, color = '#419bb9')         
#ax21.bar(ind+width/2+0.01, data.other_multiAns['waysN'], width/2, color = '#be6fa6')
#ax21.bar(ind+width*1.5, data.pnsgen_multiAns['waysN'], width/2, color = '#df884e')

nrm=mpl.colors.Normalize(-1,1)
#colors=mpl.cm.RdBu(nrm(-dz))

colours = ['r', 'g', 'c', 'y']

for i in range(0, len(colours)): 
    dz = frames[i]     
    ax1.bar3d(xpos[i], ypos[i], zpos, dx, dy, dz, color=colours[i]*len(data.global_multiAns['ways']))
    
ind = np.arange(len(data.global_multiAns['ways'])) # the x locations for the groups

ax1.set_xticks(ind+0.5)
ax1.set_yticks(np.arange(4)*2+1.5)
    
ax1.set_xticklabels(data.male_multiAns['ways'].index)
ax1.set_yticklabels(data.df['gender'].unique())
    
plt.show()