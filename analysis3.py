#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 14:48:27 2017

@author: pesa
"""
import pandas as pd
from pandas.api.types import CategoricalDtype
import matplotlib.pyplot as plt
from matplotlib import colors as c
import numpy as np
import seaborn as sns

import processData1 as data


from statsmodels.formula.api import ols

sizes = data.df_spread.groupby( [ "age", "going_out_frequency"] ).count().fillna(0)

model = ols('gender ~ dpt + 1', sizes).fit()

print(model.summary())  

#plot
#~~~~

sns.lmplot(y='age', x='going_out_frequency', data=data.df_spread.count()) 
plt.show()

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
