#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  9 10:06:51 2017

@author: pesa
"""
#plot (line)
#scatter (dots)

import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
from matplotlib import colors as c
import numpy as np

df = pd.read_csv('/Users/pesa/Google Drive/dataVis2017/Group_Survey.csv')
#df = pd.read_csv('https://docs.google.com/spreadsheets/d/1ym9TjJ7Yftu-AGzNXqCKfqlzLF6efN_qDaNXKYfniA8/gviz/tq?tqx=out:csv')

# --- SORTING DATA TYPES ---

# make timestamp into a datetime64 dtype
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp')

# rename columns, so that we can easily retrieve them by name
df.columns = ['date','ways_to_listen','active_src_plat', 'discovery_ways', 
              'last_wk_genres', 'lwg_change', 'goig_out_frequency', 'dpt',
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
                                                    '16-23', '24-29', '30-40'
                                                    '40-50', '> 50'])
df['goig_out_frequency'] = df['goig_out_frequency'].astype(
                                                    'category', ordered=True, 
                                                    categories=[
                                                    'less than 4 times a year',
                                                    'less than once a month but more than 4 times a year', 
                                                    '1-2 times per month'
                                                    '3-4 times per month', 
                                                    '5 times or more per month'])
# we record changes between last weeks' most listened genres
# and last year's by converting Yes and No to a bool with a re-map
boolMap = {'Yes': True, 'No': False}
df['lwg_change'] = df['lwg_change'].map(boolMap)

# --- SPLIT MUTLIPLE ANSWER FIELDS ----

# create new data frame by splitting the "stringified" multiple answer elements
waysDF = df['ways_to_listen'].str.split(pat=';', expand=True)
platDF = df['active_src_plat'].str.split(pat=';', expand=True)
discoverDF = df['discovery_ways'].str.split(pat=';', expand=True)
lwgDF = df['last_wk_genres'].str.split(pat=';', expand=True) 


# ------------------------

print('-----')

# count elements in the new data frame
ways_count = pd.value_counts(waysDF.values.flatten())
#print(ways_count)
# create bar chart (histogram) along x axis
ax = ways_count.plot.bar(rot=90)

# ------------------------

m = df.loc[:,'gender'] == 'Male'
f = df.loc[:,'gender'] == 'Female'
#print(m[m].index)
#print(f[f].index)



# ------------------------

#avoid labels to be cut out of the image
plt.tight_layout()

plt.show()