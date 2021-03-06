

```python
#Import Dependencies
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, inspect
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from flask import Flask, jsonify
```


```python
#Read in CSV Spreadsheets
hawaii_measurements = pd.read_csv("resources/clean_hawaii_measurements.csv")
hawaii_stations = pd.read_csv("resources/clean_hawaii_stations.csv")
```


```python
#Remove the extra index column(s)
hawaii_measurements = hawaii_measurements.rename(columns={"Unnamed: 0":"index"}).set_index('index')
hawaii_stations = hawaii_stations.rename(columns={"Unnamed: 0":"index"}).set_index('index')
```


```python
# Connect to the SQL Engine
engine = create_engine("sqlite:///hawaii.sqlite")
conn = engine.connect()
```


```python
# DEBUG: Clear the databases so I don't get errors when running the script multiple times. 
engine.execute("DELETE FROM hawaii_measurements;")
engine.execute("DELETE FROM hawaii_stations;")
```




    <sqlalchemy.engine.result.ResultProxy at 0x110e49860>




```python
# Push the dataframes to the databases: 
hawaii_measurements.to_sql(name="hawaii_measurements", con=conn, if_exists='append')
hawaii_stations.to_sql(name="hawaii_stations", con=conn, if_exists='append')
```


```python
# Grab the database's classes
Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
```


```python
# Set the classes to variables:
Measurements = Base.classes.hawaii_measurements
Station = Base.classes.hawaii_stations
```


```python
session = Session(engine)
```


```python
# Retrieve the last (most recent since it's not current) 12 months in data from the measurements database: 

data = session.query(Measurements.date, Measurements.prcp).filter(Measurements.date >= '2016-08-23').order_by(Measurements.date)
data_list = []
for row in data:
    data_list.append(row)
```


```python
# Add it to a dataframe: 

date_prcp = pd.DataFrame(data= data_list)
date_prcp = date_prcp.sort_values("date", ascending=True)
date_prcp = date_prcp.set_index("date")
date_prcp.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>prcp</th>
    </tr>
    <tr>
      <th>date</th>
      <th></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2016-08-23</th>
      <td>0.00</td>
    </tr>
    <tr>
      <th>2016-08-23</th>
      <td>0.15</td>
    </tr>
    <tr>
      <th>2016-08-23</th>
      <td>0.05</td>
    </tr>
    <tr>
      <th>2016-08-23</th>
      <td>0.02</td>
    </tr>
    <tr>
      <th>2016-08-23</th>
      <td>1.79</td>
    </tr>
  </tbody>
</table>
</div>




```python
measurements_df = pd.read_sql('SELECT * FROM hawaii_measurements', con=conn)
measurements_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>station</th>
      <th>date</th>
      <th>prcp</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>0</td>
      <td>USC00519397</td>
      <td>2010-01-01</td>
      <td>0.08</td>
      <td>65</td>
    </tr>
    <tr>
      <th>1</th>
      <td>1</td>
      <td>USC00519397</td>
      <td>2010-01-02</td>
      <td>0.00</td>
      <td>63</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2</td>
      <td>USC00519397</td>
      <td>2010-01-03</td>
      <td>0.00</td>
      <td>74</td>
    </tr>
    <tr>
      <th>3</th>
      <td>3</td>
      <td>USC00519397</td>
      <td>2010-01-04</td>
      <td>0.00</td>
      <td>76</td>
    </tr>
    <tr>
      <th>4</th>
      <td>5</td>
      <td>USC00519397</td>
      <td>2010-01-07</td>
      <td>0.06</td>
      <td>70</td>
    </tr>
  </tbody>
</table>
</div>




```python
last12months_df = pd.read_sql("SELECT * FROM hawaii_measurements WHERE date >= '2016-08-23'", con=conn)
last12months_df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>index</th>
      <th>station</th>
      <th>date</th>
      <th>prcp</th>
      <th>tobs</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2363</td>
      <td>USC00519397</td>
      <td>2016-08-23</td>
      <td>0.00</td>
      <td>81</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2364</td>
      <td>USC00519397</td>
      <td>2016-08-24</td>
      <td>0.08</td>
      <td>79</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2365</td>
      <td>USC00519397</td>
      <td>2016-08-25</td>
      <td>0.08</td>
      <td>80</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2366</td>
      <td>USC00519397</td>
      <td>2016-08-26</td>
      <td>0.00</td>
      <td>79</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2367</td>
      <td>USC00519397</td>
      <td>2016-08-27</td>
      <td>0.00</td>
      <td>77</td>
    </tr>
  </tbody>
</table>
</div>




```python
# Create a function which gives the min, max, and mean temperatures between given dates: 
def calc_temps (start_date, end_date):
    dataframe = pd.read_sql(f"SELECT * FROM hawaii_measurements WHERE (date >= '{start_date}' AND date <= '{end_date}')", con=conn)
    min_temp = dataframe['tobs'].min()
    max_temp = dataframe['tobs'].max()
    mean_temp = dataframe['tobs'].mean()
```


```python
# Convert date strings into datetime objects
converted_timestamps = []
for date in measurements_df['date']:
    converted_time = datetime.strptime(date, "%Y-%m-%d")
    converted_timestamps.append(converted_time)
converted_timestamps[10]

# Reset the date column with the datetime objects
measurements_df['date'] = converted_timestamps
```


```python
# Create the Flask API server:
app = Flask(__name__)

@app.route("/api/v1.0/precipitation")

def precipitation():
    # Create a dataframe with the that only includes the dates for the last year. 
    now = datetime.now() 
    year_ago = datetime.now() - timedelta(days=365)
    dataframe = measurements_df[(measurements_df['date'] >= year_ago) & (measurements_df['date'] <= now)]
    
    # Convert the datetime objects into strings so the dictionary can read them. 
    date_string_list = []
    for datetimeobject in dataframe.date:
        date_string_list.append(datetimeobject.strftime("%Y-%m-%d"))
    dataframe.date = date_string_list
    
    #Create the dictionary and publish it. 
    dictionary = dataframe[['date','tobs']].set_index("date").T.to_dict('list')
    return jsonify(dictionary)

@app.route("/api/v1.0/stations")

def stations():
    stations_list = hawaii_stations.station.tolist()
    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")

def tobs():
    # Create a dataframe with the that only includes the dates for the last year. 
    now = datetime.now() 
    year_ago = datetime.now() - timedelta(days=365)
    dataframe = measurements_df[(measurements_df['date'] >= year_ago) & (measurements_df['date'] <= now)]
    
    #Make a list of the temperatures and publish them
    temperature_list = dataframe['tobs'].tolist()
    return jsonify(temperature_list)

@app.route("/api/v1.0/<start>/<end>")

def custom_date(start, end=False):
    if end == False:
        dataframe = measurements_df[measurements_df['date'] >= start]
        min_temp = dataframe['tobs'].min()
        max_temp = dataframe['tobs'].max()
        mean_temp = dataframe['tobs'].mean()
        return str({"MaxTemp" : max_temp,"MinTemp" : min_temp, "MeanTemp" : mean_temp})
    else:
        dataframe = measurements_df[(measurements_df['date'] >= start) & (measurements_df['date'] <= end)]
        min_temp = dataframe['tobs'].min()
        max_temp = dataframe['tobs'].max()
        mean_temp = dataframe['tobs'].mean()
        return str({"MaxTemp" : max_temp,"MinTemp" : min_temp, "MeanTemp" : mean_temp})

@app.route("/api/v1.0/<start>")
def custom_date2(start):
    dataframe = measurements_df[measurements_df['date'] >= start]
    min_temp = dataframe['tobs'].min()
    max_temp = dataframe['tobs'].max()
    mean_temp = dataframe['tobs'].mean()
    return str({"MaxTemp" : max_temp, "MinTemp" : min_temp, "MeanTemp" : mean_temp})


if __name__ == "__main__":
    app.run(debug=True)
```

     * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
     * Restarting with stat



    An exception has occurred, use %tb to see the full traceback.


    SystemExit: 1



    /Users/ucidataanalytics/anaconda3/lib/python3.6/site-packages/IPython/core/interactiveshell.py:2870: UserWarning: To exit: use 'exit', 'quit', or Ctrl-D.
      warn("To exit: use 'exit', 'quit', or Ctrl-D.", stacklevel=1)

