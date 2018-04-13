
# coding: utf-8

# In[1]:


#Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt


# In[2]:


#Read in CSV Spreadsheets
hawaii_measurements = pd.read_csv("resources/clean_hawaii_measurements.csv")
hawaii_stations = pd.read_csv("resources/clean_hawaii_stations.csv")


# In[3]:


#Remove the extra index column(s)
hawaii_measurements = hawaii_measurements.rename(columns={"Unnamed: 0":"index"}).set_index('index')
hawaii_stations = hawaii_stations.rename(columns={"Unnamed: 0":"index"}).set_index('index')


# In[4]:


measurements_dates = hawaii_measurements['date']
measurements_dates[0]


# In[5]:


# View the dataframes
print(hawaii_measurements.head())
print(hawaii_stations.head())


# In[6]:


# Connect to the SQL Engine
engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()


# In[7]:


engine.execute("DELETE FROM hawaii_measurements;")
engine.execute("DELETE FROM hawaii_stations;")


# In[8]:


hawaii_measurements.to_sql(name="hawaii_measurements", con=conn, if_exists='append')
hawaii_stations.to_sql(name="hawaii_stations", con=conn, if_exists='append')


# In[9]:


Base = automap_base()
Base.prepare(engine, reflect=True)


# In[10]:


Base.classes.keys()


# In[11]:


Measurements = Base.classes.hawaii_measurements
Station = Base.classes.hawaii_stations


# In[12]:


session = Session(engine)


# In[13]:


data = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= '2016-08-23').order_by(Measurements.date)
data_list = []
for row in data:
    data_list.append(row)


# In[14]:


date_prcp = pd.DataFrame(data= data_list)
date_prcp = date_prcp.sort_values("date", ascending=True)
date_prcp = date_prcp.set_index("date")
date_prcp.head()


# In[15]:


#XTICK ATTEMPT WITH PLT.SUBPLOT
#x = date_prcp.index.tolist()
#y = date_prcp['prcp'].tolist()
#ax = plt.subplot(111)
#ax.bar(x, y)
#ax.xaxis_date()
#plt.show()


# In[16]:


plt.figure(figsize=(5,3))
date_prcp.plot()
plt.xlabel("Date")
plt.ylabel("Precipitation in Inches")
plt.show()


# In[17]:


measurements_df = pd.read_sql('SELECT * FROM hawaii_measurements', con=conn)
measurements_df.head()


# In[18]:


print(measurements_df['station'].nunique())


# In[19]:


print(measurements_df['station'].value_counts())


# In[20]:


last12months_df = pd.read_sql("SELECT * FROM hawaii_measurements WHERE date >= '2016-08-23'", con=conn)
last12months_df.head()


# In[21]:


plt.hist(last12months_df['tobs'], 12)
plt.xlabel("Temperature")
plt.ylabel("Frequency")
plt.show()


# In[22]:


def calc_temps (start_date, end_date):
    dataframe = pd.read_sql(f"SELECT * FROM hawaii_measurements WHERE (date >= '{start_date}' AND date <= '{end_date}')", con=conn)
    min_temp = dataframe['tobs'].min()
    max_temp = dataframe['tobs'].max()
    mean_temp = dataframe['tobs'].mean()
    
    print(min_temp)
    print(max_temp)
    print(mean_temp)
    
    plt.figure(figsize=(2,5))
    plt.bar(1, max_temp, width=1, yerr=(max_temp - min_temp), color="salmon", alpha=.5)
    plt.ylabel("Temp (F)")
    plt.title("Trip Avg Temp")
    plt.show()


# In[23]:


calc_temps("2010-01-01", "2010-12-30")


# In[24]:


from flask import Flask, jsonify


# In[25]:


# Convert date strings into datetime objects
converted_timestamps = []
for date in measurements_df['date']:
    converted_time = datetime.strptime(date, "%Y-%m-%d")
    converted_timestamps.append(converted_time)
converted_timestamps[10]

# Reset the date column with the datetime objects
measurements_df['date'] = converted_timestamps


# In[29]:


app = Flask(__name__)

@app.route("/precipitation")

def precipitation():
    now = datetime.now() 
    year_ago = datetime.now() - timedelta(days=365)
    dataframe = measurements_df[(measurements_df['date'] >= year_ago) & (measurements_df['date'] <= now)] 
    #dataframe = pd.read_sql(f"SELECT * FROM hawaii_measurements WHERE (date >= '{year_ago}' AND date <= '{now}')", con=conn)
    
    date_string_list = []
    for datetimeobject in dataframe.date:
        date_string_list.append(datetimeobject.strftime("%Y-%m-%d"))
    dataframe.date = date_string_list
    
    dictionary = dataframe[['date','tobs']].set_index("date").T.to_dict('list')
    return jsonify(dictionary)
    
if __name__ == "__main__":
    app.run(debug=True)

