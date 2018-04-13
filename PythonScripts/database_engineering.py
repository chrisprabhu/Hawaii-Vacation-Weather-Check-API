
# coding: utf-8

# In[2]:


import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import Column, Integer, String, Float, create_engine, inspect
from sqlalchemy.ext.declarative import declarative_base


# In[3]:


#Create the new sqlite database:
engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()


# In[ ]:


#Create the tables in the database using classes and declarative_base:
Base = declarative_base()
class HawaiiMeasurements(Base):
    __tablename__ = "hawaii_measurements"
    index = Column(Integer, primary_key=True)
    station = Column(String)
    date = Column(String)
    prcp = Column(Float)
    tobs = Column(Integer)
    
class HawaiiStations(Base):
    __tablename__ = "hawaii_stations"
    index = Column(Integer, primary_key=True)
    station = Column(String)
    name = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)


# In[4]:


# Push the new tables/classes to the database:    
Base.metadata.create_all(engine)


# In[4]:


#Inspect the database to make sure the tables were created succesfully:
inspector = inspect(engine)
inspector.get_table_names()


# In[5]:


# Check to see if the columns were created successfully: 
for column in inspector.get_columns("hawaii_stations"):
    print(column['name'])

