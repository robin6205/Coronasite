#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Load EDA Pkgs
import pandas as pd
import numpy as np


# In[2]:


#Load DataViz Packages
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


#Load Geopandas
import geopandas as gpd
from shapely.geometry import Point, Polygon
import descartes


# In[82]:


#load Dataset
import time
import pandas as pd
import schedule
timestr = time.strftime("%Y%m%d-%H%M%S")

confirmed_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
recovered_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
death_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

#Function to Fetch and Reshape
def get_melt_data(data_url,case_type):
    df = pd.read_csv(data_url)
    melted_df = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'])
    melted_df.rename(columns={"variable":"Date","value":case_type},inplace=True)
    return melted_df

def merge_data(confirmed_df, recovered_df, deaths_df):
    news_df = confirmed_df.merge(recovered_df)
    new_df = news_df.merge(deaths_df)
    return new_df

def fetch_data():
    #"Fetch and Prep"
    
    confirm_df = get_melt_data(confirmed_cases_url, "Confirmed")
    recovered_df = get_melt_data(recovered_cases_url,"Recovered")
    death_df = get_melt_data(death_cases_url,"Deaths")
    print("Merging Data")
    final_df = merge_data(confirm_df,recovered_df,death_df)
    print("Preview Data")
    print(final_df.tail(5))
    filename = "covid_19_merged_dataset_updated_{}.csv".format(timestr)
    print("Saving Dataset as {}".format(filename))
    #final_df.to_csv(filename)
    print("Finished")
    print (filename)
    return [death_df], [recovered_df], [confirm_df], [final_df]
#task
# schedule.every(5).seconds.do(fetch_data)
# while True:
#     schedule.run_pending()
#     time.sleep(1)


# In[83]:


if __name__ == "__main__":
    [death_df], [recovered_df], [confirm_df], [final_df] = fetch_data()


# In[76]:


#death_df.dtypes
final_df.shape


# In[31]:


#First 10
final_df.head(10)


# In[33]:


final_df.isna().sum()


# In[35]:


final_df.describe()


# In[42]:


#Number of Case Per Date/Day
df = final_df
final_df.columns


# In[51]:


df_per_day = final_df.groupby('Date')['Confirmed',
       'Recovered', 'Deaths'].sum()
# filen = "dayanalysis.csv"
# countrydeath.to_csv(filen)


# In[52]:


df_per_day.head()


# In[53]:


df_per_day.describe()


# In[64]:


#Max number of cases
df_per_day['Confirmed'].max()


# In[65]:


#Min number of cases
df_per_day['Confirmed'].min()


# In[68]:


#Date for maximum number cases
#Can be used for "Data updated on"
df_per_day['Confirmed'].idxmax()


# In[85]:


#Number of cases per country/Province
CRDdaily = df.groupby(['Country/Region'])['Confirmed',
       'Recovered', 'Deaths'].max()


# In[86]:


df.groupby(['Province/State','Country/Region'])['Confirmed',
       'Recovered', 'Deaths'].max()


# In[88]:


# Number of Data set per country
df['Country/Region'].value_counts()


# In[89]:


# Number of Data set per country
df['Country/Region'].value_counts().plot(kind='bar',figsize=(20,10))


# In[91]:


df['Country/Region'].unique()


# In[92]:


# How many country affected
len(df['Country/Region'].unique())


# In[93]:


plt.figure(figsize=(20,10))
df['Country/Region'].value_counts().plot.pie(autopct="%1.1f%%")


# # Check for distribution on the Map
# + Lat/Long
# + Geometry/Point

# In[94]:


dir(gpd)


# In[99]:


#Convert data to geodataframe
gdf01 = gpd.GeoDataFrame(df,geometry=gpd.points_from_xy(df['Long'],df['Lat']))


# In[103]:


gdf01.head()
#type(gdf01)


# In[104]:


#Method
points = [Point(x,y) for x,y in zip(df.Long,df.Lat)]


# In[107]:


gdf03 = gpd.GeoDataFrame(df,geometry=points)


# In[109]:


gdf03


# In[111]:


#Mapplot
gdf01.plot(figsize=(20,10))


# In[114]:


#Overlapping with world map
world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
ax = world.plot(figsize = (20,10))
ax.axis('off')


# In[118]:


# Overlap
fig,ax = plt.subplots(figsize = (20,10))
gdf01.plot(cmap='Purples', ax=ax)
world.geometry.boundary.plot(color=None,edgecolor='k',linewidth=2,ax=ax)


# In[120]:


#Per Country
world 


# In[122]:


world['continent'].unique()


# In[123]:


asia = world[world['continent'] == 'Asia']


# In[124]:


asia


# In[125]:


africa = world[world['continent'] == 'Africa']
north_america = world[world['continent'] == 'North America']
europe =  world[world['continent'] == 'Europe']


# In[127]:


df[df['Country/Region'] == 'China']


# In[128]:


gdf01[gdf01['Country/Region'] == 'China']


# In[129]:


# Overlap of zoom into china
fig,ax = plt.subplots(figsize = (20,10))
gdf01[gdf01['Country/Region'] == 'China'].plot(cmap='Purples', ax=ax)
world.geometry.boundary.plot(color=None,edgecolor='k',linewidth=2,ax=ax)


# In[130]:


fig,ax = plt.subplots(figsize = (20,10))
gdf01[gdf01['Country/Region'] == 'China'].plot(cmap='Purples', ax=ax)
asia.geometry.boundary.plot(color=None,edgecolor='k',linewidth=2,ax=ax)


# In[131]:


fig,ax = plt.subplots(figsize = (20,10))
gdf01[gdf01['Country/Region'] == 'India'].plot(cmap='Purples', ax=ax)
asia.geometry.boundary.plot(color=None,edgecolor='k',linewidth=2,ax=ax)


# In[132]:


fig,ax = plt.subplots(figsize = (20,10))
gdf01[gdf01['Country/Region'] == 'Egypt'].plot(cmap='Purples', ax=ax)
africa.geometry.boundary.plot(color=None,edgecolor='k',linewidth=2,ax=ax)


# In[133]:


#US Graph
fig,ax = plt.subplots(figsize = (20,10))
gdf01[gdf01['Country/Region'] == 'US'].plot(cmap='Purples', ax=ax)
north_america.geometry.boundary.plot(color=None,edgecolor='k',linewidth=2,ax=ax)


# In[135]:


#EUrope graph
fig,ax = plt.subplots(figsize = (20,10))
gdf01[gdf01['Country/Region'] == 'United Kingdom'].plot(cmap='Purples', ax=ax)
europe.geometry.boundary.plot(color=None,edgecolor='k',linewidth=2,ax=ax)


# In[ ]:





# In[136]:


#Time Series Analysis
df.head()


# In[137]:


df_per_day


# In[138]:


#Copy dataset
df2 = df
df.to_csv("Coronavirus_data_clean.csv")


# In[139]:


import datetime as dt


# In[141]:


df['cases_date'] = pd.to_datetime(df2['Date'])


# In[142]:


df2.dtypes


# In[143]:


df['cases_date'].plot(figsize=(20,10))


# In[144]:


ts = df2.set_index("cases_date")


# In[146]:


#Select for Jan
ts.loc['2020-01']


# In[147]:


ts.loc['2020-02-24':'2020-02-25']


# In[149]:


ts.loc['2020-02-24':'2020-02-25'][['Confirmed','Recovered']]


# In[151]:


ts.loc['2020-01-20':'2020-02-25'][['Confirmed','Recovered']].plot(figsize=(20,10))


# In[152]:


ts.loc['2020-01-20':'2020-02-25'][['Confirmed','Deaths']].plot(figsize=(20,10))


# In[153]:


df_by_date = ts.groupby(["cases_date"]).sum().reset_index(drop=None)


# In[154]:


df_by_date


# In[155]:


df_by_date.columns


# In[156]:


df_by_date[['Confirmed', 'Recovered', 'Deaths']].plot(kind='line',figsize=(20,10))


# In[ ]:




