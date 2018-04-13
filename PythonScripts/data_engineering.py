
# coding: utf-8

# In[1]:


import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base


# In[2]:


# Read in the CSV spreadsheets as pandas Dataframes
hawaii_measurements = pd.read_csv("resources/hawaii_measurements.csv")
hawaii_stations = pd.read_csv("resources/hawaii_stations.csv")


# In[3]:


#Inspect the dataframes:
print(hawaii_measurements.head())
print(hawaii_stations.head())


# In[4]:


#Check if there are any missing values in the dataframes:
print(hawaii_measurements.isnull().any())


# In[5]:


print(hawaii_stations.isnull().any())


# In[6]:


# Drop the missing values from hawaii_measurements:
hawaii_measurements = hawaii_measurements.dropna()


# In[7]:


#Verify the data has been dropped:
hawaii_measurements.isnull().any()


# In[8]:


#Write new CSV files with the cleaned data:
hawaii_measurements.to_csv("resources/clean_hawaii_measurements.csv")
hawaii_stations.to_csv("resources/clean_hawaii_stations.csv")

