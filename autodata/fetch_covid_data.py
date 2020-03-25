#!/usr/bin/env python
# coding: utf-8

# In[8]:


import time
import pandas as pd
import schedule
timestr = time.strftime("%Y%m%d-%H%M%S")


# In[9]:


confirmed_cases_url = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv"
recovered_cases_url ="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv"
death_cases_url ="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv"

# In[10]:


#Function to Fetch and Reshape
def get_melt_data(data_url,case_type):
    df = pd.read_csv(data_url)
    melted_df = df.melt(id_vars=['Province/State', 'Country/Region', 'Lat', 'Long'])
    melted_df.rename(columns={"variable":"Date","value":case_type},inplace=True)
    return melted_df


# In[26]:


def merge_data(confirmed_df, recovered_df, deaths_df):
    news_df = confirmed_df.merge(recovered_df)
    new_df = news_df.merge(deaths_df)
    return new_df


# In[27]:


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
    final_df.to_csv(filename)
    print("Finished")


# In[25]:


#task
schedule.every(5).seconds.do(fetch_data)
while True:
    schedule.run_pending()
    time.sleep(1)


# In[ ]:




