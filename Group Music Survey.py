import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#attempting to see if there are trends between, age, ethinicity and genre preference (eclecticism?)

df = pd.read_csv('https://docs.google.com/spreadsheets/d/1ym9TjJ7Yftu-AGzNXqCKfqlzLF6efN_qDaNXKYfniA8/gviz/tq?tqx=out:csv')




# Merge genre and ethnic to explore relationship, why isn't this working?
'''
df.index.name = 'id'
Ethnicity.index.names = ['id', 'genre_pref']
Ethnicity = Ethnicity.to_frame().join(df['Ethnicity'], how='left')
Ethnicity.columns=['genre', 'ethnicity']
Ethnicity.groupby(['genre', 'ethnicity']).size()
ax = sns.boxplot(y = Ethnicity['genre'], x = Ethnicity['ethnicity'].cat.codes, width = 0.5)
ax.set(xlabel='Ethnicity')
'''

#Genre_count.plot.barh()


#get date
df['Timestamp'] = pd.to_datetime(df['Timestamp'])
df.set_index('Timestamp')

df.columns = ['date', 'ways_to_listen', 'active_src_plat', 'discovery_ways', 'last_wk_Genres', 'last_wk_Genre_change', 'going_out_frequency', 'dpt', 'age', 'gender', 'ethnicity']
Age = df['age'] 
Age = Age.astype('category')
Age_count = Age.value_counts()

'''
platform = df['active_src_plat'].str.split(';', expand=True)
platform = platform.stack()
platform = platform.astype('category')
print(platform.value_counts())

platform.value_counts().plot.barh()
'''

'''
department = df['dpt'].str.split(';', expand=True)
department = department.stack()
department = departme
astype('category')
print(department.value_counts())

department.value_counts().plot.barh()
'''
ax = plt.subplot()
colors = 'rgbkymcb'
Ethnicity = df['ethnicity'].str.split(';', expand=True)
Ethnicity = Ethnicity.stack()
Ethnicity = Ethnicity.astype('category')
Ethnicity_count = Ethnicity.value_counts()

Ethnicity_count.plot(
	kind='barh', 
	color=colors,
)

plt.show()


Genre = df['last_wk_Genres'].str.split(';', expand=True) #split different genres from entries
Genre = Genre.stack()
Genre = Genre.astype('category')
#Age_count.plot.barh
#print(Age_count)

print(df.describe(exclude=[np.datetime64]))

#print(df.head())

#fig = plt.figure(figsize=(7, 7)) 

#df['age'] = df['age'].astype('category', ordered=True, categories=[ '16-23', '24-29', '30-40', '40-50', '> 50']) #ordered categories for age

#cols_to_transform = [ '16-23', '24-29', '30-40', '40-50', '> 50'] #get dummies
#age_with_dummies = pd.get_dummies( columns = cols_to_transform, data = df['Age_group'] )
#print(age_with_dummies)



# See genre freq dist

# Merge genre and age to explore relationship

df.index.name = 'id'
Genre.index.names = ['id', 'genre_pref']
Genre = Genre.to_frame().join(df['age'], how='left')
Genre.columns=['last_wk_Genres', 'age']
Genre.groupby(['last_wk_Genres', 'age']).size()
print(Genre) 


#ax = sns.boxplot(y = Genre['genre'], x = Genre['age'].cat.codes, width = 0.5)
#ax.set_xticklabels(['', '16-23', '', '24-29', '', '30-40', '', '40-50', '', '> 50'])
#ax.set(xlabel='Age Group')



#bubble chart
#Genre_count = Genre['genre'].value_counts()
'''
sizes = Genre['last_wk_Genres'].value_counts()

def summing(col):
	sum=0
	for indi in sizes['date']:
		sum+=indi
	return(sum)


ax = plt.subplot()
ax.scatter(Genre['age'], Genre["last_wk_Genres"], s =sizes)
'''

#sns.swarmplot(x=age_with_dummies, y=Genre_count.values, hue=Genre_count.loc, data=df)
#ax = sns.swarmplot(y=Genre_count.values, x=Genre['age'].cat.codes, color=Genre['genre']) #visualise most popular genres for each age group


#Ethnicity = df['Ethnicity'].str.split(';', expand=True)
#Ethnicity = Ethnicity.stack()
#Ethnicity = Ethnicity.astype('category')
#Ethnicity_count = Ethnicity.value_counts()
#print(Ethnicity_count)
#Ethnicity_count.plot.barh()
#plt.show()



#print(Genre_count)





#print(Genre)


#print(Genre)
#sns.heatmap(Genre, annot=True)


#print(Genre_count.values)
#sns.stripplot(x='Age_group', y=Genre_count.values, data=df)

#sns.boxplot(x="day", y="total_bill", hue="sex", data=tips, palette="PRGn")

#Genre_count.plot.bar()

#print(Genre_count) 

#try plotly...
#stacked bar charts for similar genres
#find most eclectic person?
#ancova correlation
#sci-kit learn




