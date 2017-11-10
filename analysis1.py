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

#df = pd.read_csv('/Users/pesa/Google Drive/dataVis2017/Group_Survey.csv')
df = pd.read_csv('https://docs.google.com/spreadsheets/d/1ym9TjJ7Yftu-AGzNXqCKfqlzLF6efN_qDaNXKYfniA8/gviz/tq?tqx=out:csv')

# --- SORTING DATA TYPES ---

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

# --- SPLIT MUTLIPLE ANSWER FIELDS INTO NEW DATAFRAMES ---

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
    # we return a dictionary that holds these series
    temp_dict = {'ways' : ways_count, 'plat' : plat_count,  
      'discover' : discover_count, 'lwg' : lwg_count,}
    return temp_dict

global_multiAns = splitMultiAns(df)
#print(global_multiAns['ways'])

male_multiAns = splitMultiAns(male_df)
female_multiAns = splitMultiAns(female_df)
other_multiAns = splitMultiAns(other_df)

teen_multiAns = splitMultiAns(teen_df)
twenties_multiAns = splitMultiAns(twenties_df)
thirties_multiAns = splitMultiAns(thirties_df)
plusfifty_multiAns = splitMultiAns(plusfifty_df)

# ------------------------

print('-----')


# create bar chart (histogram) along x axisto represent ways in which 
# people listen to music the most
ax = global_multiAns['ways'].plot.bar(rot=90)
plt.tight_layout()

# ------------------------

# sum all responses to the question:
# "Has your most-listened music genre changed since to a year ago?"
lwgc = pd.value_counts(df['lwg_change'].values.flatten())

explode = (0, 0.1)  # only "explode" the 2nd slice (i.e. 'Yes')
fig1, ax1 = plt.subplots() # Create a figure (top level container for all plot elements) and a set of subplots (axes)
ax1.pie(lwgc,
        explode=explode, autopct='%1.1f%%',
        shadow=True, startangle=90) # set subplot 'ax1' as a pie plot
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
ax1.legend(loc=2, labels=['yes','no']) # plot legend
ax1.set_title('Has your most-listened music genre changed since to a year ago?', fontweight="bold", size=10)
plt.tight_layout() # make sure the text is not drawn outside of the window
# ------------------------

#avoid labels to be cut out of the image

plt.show()