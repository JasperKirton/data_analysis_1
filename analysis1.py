#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 10:06:51 2017

@author: pesa
"""

import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
from matplotlib import colors as c
import numpy as np
import seaborn as sns

import processData1 as data
# ------------------------

# create Stacked bar chart (histogram) along x axis to represent ways in which 
# people listen to music the most (divided by gender)

ind = np.arange(len(data.global_multiAns['ways'])) # the x locations for the groups
width = 0.18       # the width of the bars: can also be len(x) sequence

fig2, (ax21, ax22, ax23) = plt.subplots(1, 3) # create a figure (window-object) with 3 subplots

# create all the various bar charts (using 'bottom' attribute to stack them) [normalised]
ax21.bar(ind-width*1.5-0.02, data.female_multiAns['waysN'], width, color = '#d62728') 
ax21.bar(ind-width/2-0.02, data.male_multiAns['waysN'], width, color = '#419bb9')         
ax21.bar(ind+width/2+0.02, data.other_multiAns['waysN'], width, color = '#be6fa6')
ax21.bar(ind+width*1.5+0.02, data.pnsgen_multiAns['waysN'], width, color = '#df884e')
             
ax21.legend(loc=2, labels=('Female', 'Male', 
                           'Other', 'Prefer not to say')) # plot legend

# set subplot details
ax21.set_xticks(ind)
ax21.set_yticks(np.arange(0,40,2)/100)
ax21.set_xticklabels(data.male_multiAns['ways'].index, rotation='vertical')
ax21.set_ylabel('% of people within group')
ax21.set_title('Ways of listening to music (%)')
ax21.legend(loc = 'upper left')

width2 = 0.45 
# create all the various bar charts (using 'bottom' attribute to stack them) [real vals]
p1 = ax22.bar(ind, data.female_multiAns['ways'], width2, color = '#d62728')
p1.set_label('Female')
p2 = ax22.bar(ind, data.male_multiAns['ways'], width2, bottom=data.female_multiAns['ways'],
             color = '#419bb9')
p2.set_label('Male')
p3 = ax22.bar(ind, data.other_multiAns['ways'], width2, 
             bottom = data.female_multiAns['ways'].add(data.male_multiAns['ways']), 
             color = '#be6fa6')
p3.set_label('Other')
p4 = ax22.bar(ind, data.pnsgen_multiAns['ways'], width2, 
             bottom = data.female_multiAns['ways'].add(data.male_multiAns['ways']).add(
                     data.other_multiAns['ways']), color = '#df884e')
p4.set_label('Other')



# set subplot details
ax22.set_xticks(ind)
ax22.set_yticks(np.arange(0,100,5))
ax22.set_xticklabels(data.male_multiAns['ways'].index, rotation='vertical')
ax22.set_ylabel('no of people')
ax22.set_title('Ways of listening to music (count)')
ax22.legend(loc = 'upper left')

# add a Pie showing the gender division of the survey 
gen = pd.value_counts(data.df['gender'].values.flatten())
explode2 = (0.1, 0, 0, 0)
ax23.pie(gen,
        explode=explode2, autopct='%1.1f%%',
        shadow=True, startangle=90, colors = ['#d62728', '#0589f5','#be6fa6','#df884e']) # set subplot 'ax1' as a pie plot
ax23.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax23.legend(loc=2, labels=['Female','Male', 'Other', 'Prefer not to say']) # plot legend
ax23.set_title('% of each group in tot. sample')


fig2.set_size_inches(16, 10)
fig2.set_tight_layout(True) #avoid labels to be cut out of the image
             
print('-----')

# ------------------------



# ------------------------

plt.show()