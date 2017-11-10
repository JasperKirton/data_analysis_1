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

#df = pd.read_csv('/Users/pesa/Google Drive/dataVis2017/Group_Survey.csv')
df = pd.read_csv('https://docs.google.com/spreadsheets/d/1ym9TjJ7Yftu-AGzNXqCKfqlzLF6efN_qDaNXKYfniA8/gviz/tq?tqx=out:csv')

# --- SORTING DATA TYPES & CLEANING UP ---

# make timestamp into a datetime64 dtype
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp')

# rename columns, so that we can easily retrieve them by name
df.columns = ['date','ways_to_listen','active_src_plat', 'discovery_ways', 
              'last_wk_genres', 'lwg_change', 'going_out_frequency', 'dpt',
              'age', 'gender', 'ethnicity']

# turn elements into Categoricals
df['ways_to_listen'] = df['ways_to_listen'].astype(CategoricalDtype())
df['active_src_plat'] = df['active_src_plat'].astype(CategoricalDtype())
df['discovery_ways'] = df['discovery_ways'].astype(CategoricalDtype())
df['last_wk_genres'] = df['last_wk_genres'].astype(CategoricalDtype())
df['ethnicity'] = df['ethnicity'].astype(CategoricalDtype())
# do the same for the age & going out frequency,
# but this time we make the classes ordered
df['age'] = df['age'].astype('category', ordered=True, 
                                                    categories=[
                                                    '16-23', '24-29', '30-40',
                                                    '40-50', '> 50'])
df['going_out_frequency'] = df['going_out_frequency'].astype(
                                                    'category', ordered=True, 
                                                    categories=[
                                                    'less than 4 times a year',
                                                    'less than once a month but more than 4 times a year', 
                                                    '1-2 times per month',
                                                    '3-4 times per month', 
                                                    '5 times or more per month'])
# we record changes between last weeks' most listened genres
# and last year's by converting Yes and No to a bool with a re-map
boolMap = {'Yes': True, 'No': False}
df['lwg_change'] = df['lwg_change'].map(boolMap)

# ------------------------

# Return sub-datframes with only those rows that satisfy a certain condition:

# gender
male_df = df[(df['gender'].isin(['Male']))]
female_df = df[(df['gender'].isin(['Female']))]
other_df = df[(df['gender'].isin(['Other']))]
pnsgen_df = df[(df['gender'].isin(['Prefer not to say']))]

# age
teen_df = df[(df['age'].isin(['16-23']))]
twenties_df = df[(df['age'].isin(['24-29']))]
thirties_df = df[(df['age'].isin(['30-40']))]
plusfifty_df = df[(df['age'].isin(['> 50']))]

# ethnicity
carib_df = df[(df['ethnicity'].isin(['Black British - Caribbean', 
                                    'Mixed White and Black Caribbean']))]
black_df = df[(df['ethnicity'].isin(['African or Afro-American']))]
latino_df = df[(df['ethnicity'].isin(['Latino-American']))]
asian_df = df[(df['ethnicity'].isin(['Asian or Pacific Islander']))]
brit_df = df[(df['ethnicity'].isin(['White British']))]
wother_df = df[(df['ethnicity'].isin(['White Other']))]
pnsetn_df = df[(df['ethnicity'].isin(['Prefer not to say']))]

# --- SPLIT MUTLIPLE ANSWER FIELDS INTO NEW DATAFRAMES ---

# define function to split appropriate fields in the input dataframe
def splitMultiAns (dataFrame) :
    # create new data frames to store multiple answer elements of given dataframe
    # we do this by by splitting the "string" that contains the multiple answers
    waysDF = dataFrame['ways_to_listen'].str.split(pat=';', expand=True)
    platDF = dataFrame['active_src_plat'].str.split(pat=';', expand=True)
    discoverDF = dataFrame['discovery_ways'].str.split(pat=';', expand=True)
    lwgDF = dataFrame['last_wk_genres'].str.split(pat=';', expand=True) 
    # now we group the elements in each sub-df and count them
    ways_count = pd.value_counts(waysDF.values.flatten())
    plat_count = pd.value_counts(platDF.values.flatten())
    discover_count = pd.value_counts(discoverDF.values.flatten())
    lwg_count = pd.value_counts(lwgDF.values.flatten())
    # and we do the same again but with normalised values (percentages)
    ways_countN = pd.value_counts(waysDF.values.flatten(), normalize=True)
    plat_countN = pd.value_counts(platDF.values.flatten(), normalize=True)
    discover_countN = pd.value_counts(discoverDF.values.flatten(), normalize=True)
    lwg_countN = pd.value_counts(lwgDF.values.flatten(), normalize=True)
    # we return a dictionary that holds these series
    temp_dict = {'ways' : ways_count, 'plat' : plat_count,  
      'discover' : discover_count, 'lwg' : lwg_count,
      'waysN' : ways_countN, 'platN' : plat_countN, 
      'discoverN' : discover_countN, 'lwgN' : lwg_countN }
    return temp_dict

# create dictionary containing the 4 series of counted elements in the global df
global_multiAns = splitMultiAns(df)
#print(global_multiAns['ways'])

#
def countAllElements(sub_dictionary, global_dictionary) :
    sub_dictionary['ways'] = (sub_dictionary['ways'].add(
            global_dictionary['ways'])).subtract(global_dictionary['ways']).fillna(0)
    sub_dictionary['plat'] = (sub_dictionary['plat'].add(
            global_dictionary['plat'])).subtract(global_dictionary['plat']).fillna(0)
    sub_dictionary['discover'] = (sub_dictionary['discover'].add(
            global_dictionary['discover'])).subtract(global_dictionary['discover']).fillna(0)
    sub_dictionary['lwg'] = (sub_dictionary['lwg'].add(
            global_dictionary['lwg'])).subtract(global_dictionary['lwg']).fillna(0)
    sub_dictionary['waysN'] = (sub_dictionary['waysN'].add(
            global_dictionary['ways'])).subtract(global_dictionary['ways']).fillna(0)
    sub_dictionary['platN'] = (sub_dictionary['platN'].add(
            global_dictionary['plat'])).subtract(global_dictionary['plat']).fillna(0)
    sub_dictionary['discoverN'] = (sub_dictionary['discoverN'].add(
            global_dictionary['discover'])).subtract(global_dictionary['discover']).fillna(0)
    sub_dictionary['lwgN'] = (sub_dictionary['lwgN'].add(
            global_dictionary['lwg'])).subtract(global_dictionary['lwg']).fillna(0)
    return sub_dictionary
    
# create dictionaries for the gender specific sub-dataframes
# and make sure that they report a value (even 0) for all the answers
# expressed in the global dataframe    
male_multiAns = countAllElements(splitMultiAns(male_df), global_multiAns)
female_multiAns = countAllElements(splitMultiAns(female_df), global_multiAns)
other_multiAns = countAllElements(splitMultiAns(other_df), global_multiAns)
pnsgen_multiAns = countAllElements(splitMultiAns(pnsgen_df), global_multiAns)

teen_multiAns = countAllElements(splitMultiAns(teen_df), global_multiAns)
twenties_multiAns = countAllElements(splitMultiAns(twenties_df), global_multiAns)
thirties_multiAns = countAllElements(splitMultiAns(thirties_df), global_multiAns)
plusfifty_multiAns = countAllElements(splitMultiAns(plusfifty_df), global_multiAns)

carib_multiAns = countAllElements(splitMultiAns(carib_df), global_multiAns)
black_multiAns = countAllElements(splitMultiAns(black_df), global_multiAns)
latino_multiAns = countAllElements(splitMultiAns(latino_df), global_multiAns)
asian_multiAns = countAllElements(splitMultiAns(asian_df), global_multiAns)
brit_multiAns = countAllElements(splitMultiAns(brit_df), global_multiAns)
wother_multiAns = countAllElements(splitMultiAns(wother_df), global_multiAns)
pnsetn_multiAns = countAllElements(splitMultiAns(pnsetn_df), global_multiAns)
pnsetn_multiAns = countAllElements(splitMultiAns(pnsetn_df), global_multiAns)


# ------------------------

# Pie chart showing whether taste has changed

# sum all responses to the question:
# "Has your most-listened music genre changed since to a year ago?"
lwgc = pd.value_counts(df['lwg_change'].values.flatten())
lwgc_male = pd.value_counts(male_df['lwg_change'].values.flatten())
lwgc_female = pd.value_counts(female_df['lwg_change'].values.flatten())
lwgc_other = pd.value_counts(other_df['lwg_change'].values.flatten())

explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Yes')
fig1, ((ax1,ax2),(ax3,ax4)) = plt.subplots(2,2) # Create a figure (top level container for all plot elements) and a set of subplots (axes)

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

fig1.suptitle('Has your most-listened music genre changed since to a year ago?', 
              y=1.0, fontweight="bold", size=10)
fig1.set_tight_layout(True) # make sure the text is not drawn outside of the window
fig1.set_size_inches(8, 6)

# ------------------------

# create Stacked bar chart (histogram) along x axis to represent ways in which 
# people listen to music the most (divided by gender)

ind = np.arange(len(global_multiAns['ways'])) # the x locations for the groups
width = 0.18       # the width of the bars: can also be len(x) sequence

fig2, (ax21, ax22, ax23) = plt.subplots(1, 3) # create a figure (window-object) with 3 subplots

# create all the various bar charts (using 'bottom' attribute to stack them) [normalised]
ax21.bar(ind-width*1.5-0.02, female_multiAns['waysN'], width, color = '#d62728') 
ax21.bar(ind-width/2-0.02, male_multiAns['waysN'], width, color = '#419bb9')         
ax21.bar(ind+width/2+0.02, other_multiAns['waysN'], width, color = '#be6fa6')
ax21.bar(ind+width*1.5+0.02, pnsgen_multiAns['waysN'], width, color = '#df884e')
             
ax21.legend(loc=2, labels=('Female', 'Male', 
                           'Other', 'Prefer not to say')) # plot legend

# set subplot details
ax21.set_xticks(ind)
ax21.set_yticks(np.arange(0,40,2)/100)
ax21.set_xticklabels(male_multiAns['ways'].index, rotation='vertical')
ax21.set_ylabel('% of people within group')
ax21.set_title('Ways of listening to music (%)')
ax21.legend(loc = 'upper left')

width2 = 0.45 
# create all the various bar charts (using 'bottom' attribute to stack them) [real vals]
p1 = ax22.bar(ind, female_multiAns['ways'], width2, color = '#d62728')
p1.set_label('Female')
p2 = ax22.bar(ind, male_multiAns['ways'], width2, bottom=female_multiAns['ways'],
             color = '#419bb9')
p2.set_label('Male')
p3 = ax22.bar(ind, other_multiAns['ways'], width2, 
             bottom = female_multiAns['ways'].add(male_multiAns['ways']), 
             color = '#be6fa6')
p3.set_label('Other')
p4 = ax22.bar(ind, pnsgen_multiAns['ways'], width2, 
             bottom = female_multiAns['ways'].add(male_multiAns['ways']).add(
                     other_multiAns['ways']), color = '#df884e')
p4.set_label('Other')

print(np.array(female_multiAns['ways']))

# set subplot details
ax22.set_xticks(ind)
ax22.set_yticks(np.arange(0,100,5))
ax22.set_xticklabels(male_multiAns['ways'].index, rotation='vertical')
ax22.set_ylabel('no of people')
ax22.set_title('Ways of listening to music (count)')
ax22.legend(loc = 'upper left')

# add a Pie showing the gender division of the survey 
gen = pd.value_counts(df['gender'].values.flatten())
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