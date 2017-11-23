#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 20:45:56 2017

@author: pesa
"""


import pandas as pd
from pandas.api.types import CategoricalDtype

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
df['dpt'] = df['dpt'].astype(CategoricalDtype())
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

def splitAndAttach(df, name = 'target column', newcol_names = ['columns']) :
    # Creating a single dataframe for all the data 
    # (splitting multiple answers into separate columns)

    # Test Step 1: Split the ways_to_listen column from a string into a list
    #w1_test = df_copy['ways_to_listen'].str.split(pat=';')

    # Step 2: Same as test above but introducing a dummy matrix
    # to keep track of for where the multiple answer values exist
    #w1_test2 = df_copy['ways_to_listen'].str.split(pat=';').apply(lambda x: pd.Series(1, index=x))

    # Step 3 (final): we fill the nans to 0, then astype to bool to make True/False
    # we then rename new columns if apripriate and concatate it 
    # to the original frame whilst dropping the old original column
    w1 = df[name].str.split(pat=';').apply(lambda x: pd.Series(1,
            index=x)).fillna(0).astype(bool)
    if newcol_names != ['columns'] :
        w1.columns = newcol_names
    return(pd.concat([df, w1], axis=1).drop([name], axis =1))
    

# Apply above function to turn all mutliple answer fields into bool charts
# and then connect them all into one expanded dataframe with 
# multiple answer fields "flattened" across the column axis
    
df_spread = splitAndAttach(df, 'ways_to_listen', 
                     ['listening/cd', 'listening/cassette', 'listening/events', 
                      'listening/lossless','listening/lossy', 'listening/radio', 
                      'listening/streaming', 'listening/tv', 'listening/vinyl'])
    
df_spread = splitAndAttach(df_spread, 'active_src_plat', 
                     ['platform/bandcamp', 'platform/discogs', 'platform/melon', 
                      'platform/blogs', 'platform/charts', 'platform/onlineshops',
                      'platform/shazam', 'platform/socials', 
                      'platform/soundcloud','platfform/spotify', 'platform/tv', 
                      'platform/youtube', 'platform/itunes',
                      'platform/physicalshops'])
    
df_spread = splitAndAttach(df_spread, 'discovery_ways',
                     ['discover/adverts', 'discover/live', 'discover/blogs', 
                      'discover/mixes',
                      'discover/friends',
                      'discover/onlinerecommend','discover/coffeeshopplaylists', 
                      'discover/radio', 'discover/shazam',
                      'discover/soundtracks', 'discover/tv'])

df_spread = splitAndAttach(df_spread, 'last_wk_genres',
                     ['lwg/afriasian', 'lwg/classics', 'lwg/contempexp', 
                      'lwg/edm', 'lwg/idm', 'lwg/funksoul',
                      'lwg/grime', 'lwg/hiphop', 
                      'lwg/indiealt','lwg/instrum', 
                      'lwg/jazz', 'lwg/latin', 'lwg/metalpunk',
                      'lwg/mtheatre', 'lwg/popchart', 'lwg/reg',
                      'lwg/rock', 'lwg/soca', 'lwg/soundtrack',
                      'lwg/worldfolk'])
                     
# ------------------------

# create a dataframe that groups indeces by groups (eg. by gender),
# looks across the "spread out" columns of a multiple answer question
# and counts the instances where a memeber of each group indicated
# "True" or "1" for the respective multiple answer column
# -- Return normalised values not actual counts --
def bgClusteredPreference(in_df, array_of_columns_names, class_to_group_by) : 
    all_counts = []
    for ways in array_of_columns_names :
        all_counts.append(in_df.groupby(class_to_group_by)[ways].value_counts())
    # these passages below are basically to only return the dataframe
    # showing the count of "1" (or "True") instances    
    temp_df = pd.DataFrame(all_counts).T
    temp_df = temp_df.sort_index(level=1, ascending=False)
    temp_df = temp_df.head(int(temp_df.shape[0]/2)).fillna(0)
    temp_df = (temp_df.groupby(level=0).sum()).T
    temp_df2 = temp_df.copy()
    # normalize across the responses of the grouped class
    for col in temp_df.columns:
        temp_df2[col] = temp_df[col] / temp_df[col].sum()
    # return both the normalised and the count-based dataframes    
    return (temp_df.T, temp_df2.T)

# method to create a dictionary of dataframes
# each being indexed by the classes which we can use to group people
# who took part in our survey based on their background
# and having the columns belonging to 1 multiple answer group     
def countTablesByGroups(df, array_of_classes_to_group_by, array_of_columns_names) : 
    dict_counts = {}
    dict_countsN = {}
    ind = 0
    for d in array_of_classes_to_group_by :
        dcount, dnorm = bgClusteredPreference(
                df, array_of_columns_names, array_of_classes_to_group_by[ind])
        dict_counts[array_of_classes_to_group_by[ind]] = dcount
        dict_countsN[array_of_classes_to_group_by[ind]] = dnorm
        ind+=1
    # return 2 dict: 1 with the counts and 1 normalised
    return (dict_counts, dict_countsN)

# classes
groups = ['dpt', 'age', 'gender', 'ethnicity']

listeningCols = ['listening/cd', 'listening/cassette', 'listening/events', 
                 'listening/lossless','listening/lossy', 'listening/radio', 
                 'listening/streaming', 'listening/tv', 'listening/vinyl']

listening_countsC, listening_counts = countTablesByGroups(df_spread, groups, listeningCols)

platformCols = ['platform/bandcamp', 'platform/discogs', 'platform/melon', 
                      'platform/blogs', 'platform/charts', 'platform/onlineshops',
                      'platform/shazam', 'platform/socials', 
                      'platform/soundcloud','platfform/spotify', 'platform/tv', 
                      'platform/youtube', 'platform/itunes',
                      'platform/physicalshops']

plat_countsC, plat_counts = countTablesByGroups(df_spread, groups, platformCols)

discoverCols = ['discover/adverts', 'discover/live', 'discover/blogs', 
                'discover/mixes', 'discover/friends',
                'discover/onlinerecommend','discover/coffeeshopplaylists', 
                'discover/radio', 'discover/shazam',
                'discover/soundtracks', 'discover/tv']

discover_countsC, discover_counts = countTablesByGroups(df_spread, groups, discoverCols)

lwgCols = ['lwg/afriasian', 'lwg/classics', 'lwg/contempexp', 
                      'lwg/edm', 'lwg/idm', 'lwg/funksoul',
                      'lwg/grime', 'lwg/hiphop', 
                      'lwg/indiealt','lwg/instrum', 
                      'lwg/jazz', 'lwg/latin', 'lwg/metalpunk',
                      'lwg/mtheatre', 'lwg/popchart', 'lwg/reg',
                      'lwg/rock', 'lwg/soca', 'lwg/soundtrack',
                      'lwg/worldfolk']

lwg_countsC, lwg_counts = countTablesByGroups(df_spread, groups, lwgCols)

#print(listening_counts['dpt'])

# ------------------------

# some useful arrays of labels

ways_of_listening = ['cd', 'cassette', 'live events', 'lossless digital files',
           'lossy digital files', 'radio', 'streaming', 'tv', 'vinyl']

platform_to_search = ['bandcamp', 'discogs', 'live events', 'melon',
           'blogs', 'charts', 'onlineshops', 'shazam', 'social networks',
           'soundcloud', 'spotify', 'tv', 'youtube', 'itunes',
           'physical shops']

passive_discovery_channels = ['adverts', 'live', 'blogs', 
                              'DJ mixes', 'friends',
                              'online recommendation services', 
                              'coffee shop playlists', 'radio',
                              'shazam', 'soundtracks', 'tv' ]

last_week_top_genre = ['African/Asian', 'Classical', 'Contemporary/Experimental', 
                       'Dance Music (Electronic)', 'Electronica/IDM', 
                       'Funk/Soul', 'Grime', 'Hip-Hop/Rap/R&B', 'Indie/Alternative',
                       'Instrumental', 'Jazz/Blues', 'Latin/Brazil', 'Metal/Hard-Rock/Punk', 
                       'Musical Theatre', 'Pop/Chart', 'Reggae/Dancehall', 'Rock/Country', 'Soca', 
                       'Soundtrack', 'World/Folk'] 

