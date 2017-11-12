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

# create Stacked & Grouped bar charts (histogram) along x axis to represent ways in which 
# people listen to music the most (divided by gender)

ind = np.arange(len(data.global_multiAns['ways'])) # the x locations for the groups
width = 0.15       # the width of the bars: can also be len(x) sequence

fig1, (ax21, ax22, ax23) = plt.subplots(1, 3) # create a figure (window-object) with 3 subplots

# create all the various bar charts (using 'bottom' attribute to stack them) [normalised]
ax21.bar(ind-width*1.5-0.01, data.female_multiAns['waysN'], width, color = '#d62728') 
ax21.bar(ind-width/2-0.01, data.male_multiAns['waysN'], width, color = '#419bb9')         
ax21.bar(ind+width/2+0.01, data.other_multiAns['waysN'], width/2, color = '#be6fa6')
ax21.bar(ind+width*1.5, data.pnsgen_multiAns['waysN'], width/2, color = '#df884e')
             
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
p21 = ax22.bar(ind, data.female_multiAns['ways'], width2, color = '#d62728')
p21.set_label('Female')
p22 = ax22.bar(ind, data.male_multiAns['ways'], width2, bottom=data.female_multiAns['ways'],
             color = '#419bb9')
p22.set_label('Male')
p23 = ax22.bar(ind, data.other_multiAns['ways'], width2, 
             bottom = data.female_multiAns['ways'].add(data.male_multiAns['ways']), 
             color = '#be6fa6')
p23.set_label('Other')
p24 = ax22.bar(ind, data.pnsgen_multiAns['ways'], width2, 
             bottom = data.female_multiAns['ways'].add(data.male_multiAns['ways']).add(
                     data.other_multiAns['ways']), color = '#df884e')
p24.set_label('Other')



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


fig1.set_size_inches(18, 10)
fig1.set_tight_layout(True) #avoid labels to be cut out of the image
             

# ------------------------

# create Stacked & Grouped bar charts (histogram) along x axis to represent the platform 
# that people use to listen to music (divided by gender)

ind = np.arange(len(data.global_multiAns['plat'])) # the x locations for the groups
width = 0.18       # the width of the bars: can also be len(x) sequence

fig2, (ax31, ax32) = plt.subplots(1, 2) # create a figure (window-object) with 3 subplots

# create all the various bar charts (using 'bottom' attribute to stack them) [normalised]
ax31.bar(ind-width*1.5-0.02, data.female_multiAns['platN'], width, color = '#d62728') 
ax31.bar(ind-width/2-0.02, data.male_multiAns['platN'], width, color = '#419bb9')         
ax31.bar(ind+width/2+0.02, data.other_multiAns['platN'], width/2, color = '#be6fa6')
ax31.bar(ind+width*1.5, data.pnsgen_multiAns['platN'], width/2, color = '#df884e')
             
ax31.legend(loc=2, labels=('Female', 'Male', 
                           'Other', 'Prefer not to say')) # plot legend

# set subplot details
ax31.set_xticks(ind)
ax31.set_yticks(np.arange(0,65,5)/100) # set y measuring marks
ax31.set_xticklabels(data.male_multiAns['platN'].index, rotation='vertical')
ax31.set_ylabel('% of people within group')
ax31.set_title('Platform of music experience (%)')
ax31.legend(loc = 'upper left')

width2 = 0.45 
# create all the various bar charts (using 'bottom' attribute to stack them) [real vals]
p31 = ax32.bar(ind, data.female_multiAns['plat'], width2, color = '#d62728')
p31.set_label('Female')
p32 = ax32.bar(ind, data.male_multiAns['plat'], width2, bottom=data.female_multiAns['plat'],
             color = '#419bb9')
p32.set_label('Male')
p33 = ax32.bar(ind, data.other_multiAns['plat'], width2, 
             bottom = data.female_multiAns['plat'].add(data.male_multiAns['plat']), 
             color = '#be6fa6')
p33.set_label('Other')
p34 = ax32.bar(ind, data.pnsgen_multiAns['plat'], width2, 
             bottom = data.female_multiAns['plat'].add(data.male_multiAns['plat']).add(
                     data.other_multiAns['plat']), color = '#df884e')
p34.set_label('Other')

# set subplot details
ax32.set_xticks(ind)
ax32.set_yticks(np.arange(0,100,5))
ax32.set_xticklabels(data.male_multiAns['plat'].index, rotation='vertical')
ax32.set_ylabel('no of people')
ax32.set_title('Platform of music experience (count)')
ax32.legend(loc = 'upper left')

fig2.set_size_inches(16, 10)
fig2.set_tight_layout(True) #avoid labels to be cut out of the image

# ------------------------

# Pie chart showing whether music taste has changed 
# (comparing last week's most listened to genre to 1 year ago)

# sum all responses to the question:
# "Has your most-listened music genre changed since to a year ago?"
lwgc = pd.value_counts(data.df['lwg_change'].values.flatten())
lwgc_male = pd.value_counts(data.male_df['lwg_change'].values.flatten())
lwgc_female = pd.value_counts(data.female_df['lwg_change'].values.flatten())
lwgc_other = pd.value_counts(data.other_df['lwg_change'].values.flatten())

explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Yes')
fig3, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2) # Create a figure (top level container for all plot elements) and a set of subplots (axes)

def pieFunc1 (subplot, group, title='', inlabels=['yes','no']) :
    subplot.pie(group,
            explode=explode, autopct='%1.1f%%',
            shadow=True, startangle=90) # set subplot 'ax1' as a pie plot
    subplot.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    subplot.legend(loc=2, labels=inlabels) # plot legend
    subplot.set_title(title, size=10)

pieFunc1(ax1, lwgc, 'global')
pieFunc1(ax2, lwgc_male, 'male')
pieFunc1(ax3, lwgc_female, 'female')
pieFunc1(ax4, lwgc_other, 'other')

fig3.suptitle('Has your most-listened music genre changed since to a year ago?', 
              y=1.0, fontweight="bold", size=10)
fig3.set_tight_layout(True) # make sure the text is not drawn outside of the window
fig3.set_size_inches(8, 6)

# ------------------------

# create Stacked & Grouped bar charts (histogram) along x axis to represent 
# Last Week most listened to genre (divided by gender)

ind = np.arange(len(data.global_multiAns['lwg'])) # the x locations for the groups
width = 0.2       # the width of the bars: can also be len(x) sequence

fig4, (ax41, ax42) = plt.subplots(1, 2) # create a figure (window-object) with 3 subplots

# create all the various bar charts (using 'bottom' attribute to stack them) [normalised]
ax41.bar(ind-width*1.5-0.01, data.female_multiAns['lwgN'], width, color = '#d62728') 
ax41.bar(ind-width/2-0.01, data.male_multiAns['lwgN'], width, color = '#419bb9')         
ax41.bar(ind+width/2+0.01, data.other_multiAns['lwgN'], width/2, color = '#be6fa6')
ax41.bar(ind+width*1.5-0.1, data.pnsgen_multiAns['lwgN'], width/2, color = '#df884e')
             
ax41.legend(loc=2, labels=('Female', 'Male', 
                           'Other', 'Prefer not to say')) # plot legend

# set subplot details
ax41.set_xticks(ind)
ax41.set_yticks(np.arange(0,34,2)/100) # set y measuring marks
ax41.set_xticklabels(data.male_multiAns['lwgN'].index, rotation='vertical')
ax41.set_ylabel('% of people within group')
ax41.set_title('Last Week most listened to genre (%)')
ax41.legend(loc = 'upper left')

width2 = 0.45 
# create all the various bar charts (using 'bottom' attribute to stack them) [real vals]
p41 = ax42.bar(ind, data.female_multiAns['lwg'], width2, color = '#d62728')
p41.set_label('Female')
p42 = ax42.bar(ind, data.male_multiAns['lwg'], width2, bottom=data.female_multiAns['lwg'],
             color = '#419bb9')
p42.set_label('Male')
p43 = ax42.bar(ind, data.other_multiAns['lwg'], width2, 
             bottom = data.female_multiAns['lwg'].add(data.male_multiAns['lwg']), 
             color = '#be6fa6')
p43.set_label('Other')
p44 = ax42.bar(ind, data.pnsgen_multiAns['lwg'], width2, 
             bottom = data.female_multiAns['lwg'].add(data.male_multiAns['lwg']).add(
                     data.other_multiAns['lwg']), color = '#df884e')
p44.set_label('Other')

# set subplot details
ax42.set_xticks(ind)
ax42.set_yticks(np.arange(0,50,5))
ax42.set_xticklabels(data.male_multiAns['lwg'].index, rotation='vertical')
ax42.set_ylabel('no of people')
ax42.set_title('Last Week most listened to genre (count)')
ax42.legend(loc = 'upper left')

fig4.set_size_inches(20, 10)
fig4.set_tight_layout(True) #avoid labels to be cut out of the image


# ------------------------

# create Stacked & Grouped bar charts (histogram) along x axis to represent 
# the way people discover new music (divided by gender)

ind = np.arange(len(data.global_multiAns['discover'])) # the x locations for the groups
width5 = 0.2       # the width of the bars: can also be len(x) sequence

fig5, (ax51, ax52) = plt.subplots(1, 2) # create a figure (window-object) with 3 subplots

# create all the various bar charts (using 'bottom' attribute to stack them) [normalised]
ax51.bar(ind-width*1.5-0.01, data.female_multiAns['discoverN'], width5, color = '#d62728') 
ax51.bar(ind-width/2-0.01, data.male_multiAns['discoverN'], width5, color = '#419bb9')         
ax51.bar(ind+width/2+0.01, data.other_multiAns['discoverN'], width5/2, color = '#be6fa6')
ax51.bar(ind+width*1.5-0.1, data.pnsgen_multiAns['discoverN'], width5/2, color = '#df884e')
             
ax51.legend(loc=2, labels=('Female', 'Male', 
                           'Other', 'Prefer not to say')) # plot legend

# set subplot details
ax51.set_xticks(ind)
ax51.set_yticks(np.arange(0,34,2)/100) # set y measuring marks
ax51.set_xticklabels(data.male_multiAns['discoverN'].index, rotation='vertical')
ax51.set_ylabel('% of people within group')
ax51.set_title('Ways people passively discover new music (%)')
ax51.legend(loc = 'upper left')

width52 = 0.45 
# create all the various bar charts (using 'bottom' attribute to stack them) [real vals]
p51 = ax52.bar(ind, data.female_multiAns['discover'], width52, color = '#d62728')
p51.set_label('Female')
p52 = ax52.bar(ind, data.male_multiAns['discover'], width52, bottom=data.female_multiAns['discover'],
             color = '#419bb9')
p52.set_label('Male')
p53 = ax42.bar(ind, data.other_multiAns['discover'], width52, 
             bottom = data.female_multiAns['discover'].add(data.male_multiAns['discover']), 
             color = '#be6fa6')
p53.set_label('Other')
p54 = ax42.bar(ind, data.pnsgen_multiAns['discover'], width52, 
             bottom = data.female_multiAns['discover'].add(data.male_multiAns['discover']).add(
                     data.other_multiAns['discover']), color = '#df884e')
p54.set_label('Other')

# set subplot details
ax52.set_xticks(ind)
ax52.set_yticks(np.arange(0,50,5))
ax52.set_xticklabels(data.male_multiAns['discover'].index, rotation='vertical')
ax52.set_ylabel('no of people')
ax52.set_title('Ways people passively discover new music (count)')
ax52.legend(loc = 'upper left')

fig5.set_size_inches(20, 10)
fig5.set_tight_layout(True) #avoid labels to be cut out of the image

# ------------------------

# use seaborn now:

# Plot grouped bar chart of the count of people (divided by gender)
# that go out to live music events at a certian "frequency"

fig6 = plt.figure()

graph1 = sns.factorplot(x='going_out_frequency', hue='gender',
                        data=data.df_spread, palette="BuPu",
                        kind="count", size=8, aspect = 0.6, legend=False)
graph1.set_xticklabels(rotation=90)

graph1.set_axis_labels("", "No of People")

for ax in graph1.axes.flat:
    ax.legend(loc='upper right')
    

graph1.fig.suptitle('How often do you go out for music events?',  
                    fontweight="bold", y = 1.002)
graph1.fig.set_tight_layout(True)

plt.show()