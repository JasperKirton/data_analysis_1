#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 12 14:26:09 2017

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


w_df = data.df_spread.copy()


# ------------------------

# Plot responsed over time (total count of survey submissions by day)
# NOTE: Commented out as non relevant

#fig2 = plt.figure()

# different plot to show the number of responses received across 5 days
# at day 2 we posted on the goldsmiths students FB group

# create dummy column filled with 1s
#w_df['count'] = 1
#total_results = w_df.set_index('date')

# count 1s in the dummy column
#running_results = total_results.groupby(pd.TimeGrouper('D'))['count'].count().cumsum()

# use a series of integers as long as the days of the survey
#step = pd.Series(range(0,len(running_results)), name='Days')
#graph2 = sns.tsplot(running_results, value='Total Responses', 
#                    time=step, color='husl')

#fig2.suptitle('Responses for our survey',  
#                    fontweight="bold", y = 1.002)

# ------------------------

# Use seaborn's heatmap to visualise relationships between
# people's cultural background (ethnicity / department at uni)
# and ways to experience music

# ------------------------

fig3 = plt.figure()

ax3 = plt.subplot()

graph3 = sns.heatmap(data.discover_counts['dpt'], annot=True, ax = ax3)
#graph3 = sns.clustermap(data.dicover_counts['age'], annot=True)

labelsx = data.passive_discovery_channels
labelsy = data.discover_counts['dpt'].index
ax3.set_xticklabels(labelsx, rotation='vertical')
ax3.set_yticklabels(labelsy, rotation='horizontal')
fig3.set_tight_layout(True)
fig3.set_size_inches(18, 10)
fig3.suptitle('How do you most often discover new music without searching for it?',  
                    fontweight="bold", y = 1.002)

# -----------------------
# -----------------------

fig4 = plt.figure()

ax4 = plt.subplot()

graph4 = sns.heatmap(data.listening_counts['dpt'], annot=True, ax = ax4)
#graph3 = sns.clustermap(data.dicover_counts['age'], annot=True)

labelsx4 = data.ways_of_listening
labelsy4 = data.listening_counts['dpt'].index
ax4.set_xticklabels(labelsx4, rotation='vertical')
ax4.set_yticklabels(labelsy4, rotation='horizontal')
fig4.set_tight_layout(True)
fig4.set_size_inches(18, 10)
fig4.suptitle('In which ways do you usually listen to music?',  
                    fontweight="bold", y = 1.002)


# -----------------------
# -----------------------

fig5 = plt.figure()

ax5 = plt.subplot()

graph5 = sns.heatmap(data.plat_counts['dpt'], annot=True, ax = ax5)
#graph3 = sns.clustermap(data.dicover_counts['age'], annot=True)

labelsx5 = data.platform_to_search
labelsy5 = data.plat_counts['dpt'].index
ax5.set_xticklabels(labelsx5, rotation='vertical')
ax5.set_yticklabels(labelsy5, rotation='horizontal')
fig5.set_tight_layout(True)
fig5.set_size_inches(18, 10)
fig5.suptitle('Which platforms do you use to search for new music?',  
                    fontweight="bold", y = 1.002)

# -----------------------
# -----------------------

fig6 = plt.figure()

ax6 = plt.subplot()

graph6 = sns.heatmap(data.lwg_counts['dpt'], annot=True, ax = ax6)
#graph3 = sns.clustermap(data.dicover_counts['age'], annot=True)

labelsx6 = data.last_week_top_genre
labelsy6 = data.lwg_counts['dpt'].index
ax6.set_xticklabels(labelsx6, rotation='vertical')
ax6.set_yticklabels(labelsy6, rotation='horizontal')
fig6.set_tight_layout(True)
fig6.set_size_inches(18, 10)
fig6.suptitle('Which music genres have you mostly listened to in the last week?',  
                    fontweight="bold", y = 1.002)

# -----------------------
# -----------------------

fig7 = plt.figure()

ax7 = plt.subplot()

graph7 = sns.heatmap(data.lwg_counts['ethnicity'], annot=True, ax = ax7)
#graph3 = sns.clustermap(data.dicover_counts['age'], annot=True)

labelsx7 = data.last_week_top_genre
labelsy7 = data.lwg_counts['ethnicity'].index
ax7.set_xticklabels(labelsx7, rotation='vertical')
ax7.set_yticklabels(labelsy7, rotation='horizontal')
fig7.set_tight_layout(True)
fig7.set_size_inches(18, 10)
fig7.suptitle('Which music genres have you mostly listened to in the last week?',  
                    fontweight="bold", y = 1.002)

# -----------------------
# -----------------------
# -----------------------
# -----------------------

# visualise a bubble chart showing the frequency 
# of going out to live music events in relation to one's age

fig8 = plt.figure()

ax8 = plt.subplot()

sizes = data.df_spread.groupby( [ "age", "going_out_frequency"] ).count().fillna(0)

def summing(col):
    su=0
    for indi in sizes['date']:
        su+=indi  
    return(su)

colour = [
            [0.1,0.9,0.1],
            [0.1,0.9,0.7],
            [0.8,0.9,0.1],
            [0.3,0.2,0.1],
            [0.1,0.4,0.6]
         ]

ax8.scatter(data.df_spread['age'], data.df_spread['going_out_frequency'], 
            s=((sizes['date']/summing(sizes['date']))*100)**2, c=colour)

fig8.set_tight_layout(True)
fig8.set_size_inches(8, 6)
fig8.suptitle('How often do you go out for live music events?',  
                    fontweight="bold", y = 1.002)


# -----------------------
# -----------------------
# -----------------------
# -----------------------

# Box Plot

# Build a collection of collections (expressed as pandas DF)
# each holding a sequence of values
# These values are the number of people belonging to a certain group/class 
# (e.g. gender, department, ethnicity...)

def buildArrOfColl(dictionary, key_name, array_of_column_names):
    ind = 0
    coll = dictionary[key_name][array_of_column_names[ind]]
    for ind in range (1, len(array_of_column_names)) :
        coll = pd.concat((coll, dictionary[key_name][array_of_column_names[ind]]), axis=1)
    return coll.T

#if you change the line below to data.discover_countsC
#you get a non-normalised count of people's answers
dictionary_of_subDfs = data.discover_counts

indeces_list = data.discoverCols

data_to_plot = buildArrOfColl(dictionary_of_subDfs, 'dpt', indeces_list)

# Create a figure instance and a 2D array of axes
fig9, ax_arr = plt.subplots(2, 2)

# Create the boxplot by checking what is the average 
# number of people per class that has a certain characteristic
# (in this case it can be a music consumption/discovery way)
bp1 = ax_arr[0, 0].boxplot(data_to_plot, patch_artist = True)
ax_arr[0, 0].set_xticklabels(data.passive_discovery_channels, rotation='vertical')
ax_arr[0, 0].set_ylabel('% of people per department')
            
# -----------------------

data_to_plot2 = buildArrOfColl(dictionary_of_subDfs, 'age', indeces_list)

# Create the boxplot by checking what is the average 
# number of people per class that has a certain characteristic
# (in this case it can be a music consumption/discovery way)
bp2 = ax_arr[1, 0].boxplot(data_to_plot2, patch_artist = True)
ax_arr[1, 0].set_xticklabels(data.passive_discovery_channels, rotation='vertical')
ax_arr[1, 0].set_ylabel('% of people per age group')            

# -----------------------

data_to_plot3 = buildArrOfColl(dictionary_of_subDfs, 'gender', indeces_list)

# Create the boxplot by checking what is the average 
# number of people per class that has a certain characteristic
# (in this case it can be a music consumption/discovery way)
bp3 = ax_arr[0, 1].boxplot(data_to_plot3, patch_artist = True)
ax_arr[0, 1].set_xticklabels(data.passive_discovery_channels, rotation='vertical')
ax_arr[0, 1].set_ylabel('% of people per gender group')
         
# -----------------------
data_to_plot4 = buildArrOfColl(dictionary_of_subDfs, 'ethnicity', indeces_list)

# Create the boxplot by checking what is the average 
# number of people per class that has a certain characteristic
# (in this case it can be a music consumption/discovery way)
bp4 = ax_arr[1, 1].boxplot(data_to_plot4, patch_artist = True)
ax_arr[1, 1].set_xticklabels(data.passive_discovery_channels, rotation='vertical')
ax_arr[1, 1].set_ylabel('% of people per ethnic group')
            
# -----------------------
         
colours = ['#df884e', '#1b9e77', '#c24edf', '#e15b5b' ]   
## change outline color, fill color and linewidth of the boxes
col_i=0
for bplot in (bp1, bp2, bp3, bp4) :
    col = colours[col_i]
    for box in bplot['boxes'] :
        # change outline color
        box.set( color='#7570b3', linewidth=2)
        # change fill color
        box.set( facecolor = col )
    ## change color and linewidth of the whiskers
    for whisker in bplot['whiskers']:
        whisker.set(color='#7570b3', linewidth=2)
    ## change color and linewidth of the caps
    for cap in bplot['caps']:
        cap.set(color='#7570b3', linewidth=2)
    ## change color and linewidth of the medians
    for median in bplot['medians']:
        median.set(color='#b2df8a', linewidth=2)
    ## change the style of fliers and their fill
    for flier in bplot['fliers']:
        flier.set(marker='o', color='#e7298a', alpha=0.5) 
    col_i+=1
            

fig9.set_tight_layout(True)
fig9.set_size_inches(16, 12)
fig9.suptitle('Exploring trends in ways to discover music across groups',  
                    fontweight="bold", y = 1.000)

# -----------------------
# -----------------------

plt.show()