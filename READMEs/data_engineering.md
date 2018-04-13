

```python
import pandas as pd
import pymysql
pymysql.install_as_MySQLdb()
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
```


```python
# Read in the CSV spreadsheets as pandas Dataframes
hawaii_measurements = pd.read_csv("resources/hawaii_measurements.csv")
hawaii_stations = pd.read_csv("resources/hawaii_stations.csv")
```


```python
#Inspect the dataframes:
print(hawaii_measurements.head())
print(hawaii_stations.head())
```

           station        date  prcp  tobs
    0  USC00519397  2010-01-01  0.08    65
    1  USC00519397  2010-01-02  0.00    63
    2  USC00519397  2010-01-03  0.00    74
    3  USC00519397  2010-01-04  0.00    76
    4  USC00519397  2010-01-06   NaN    73
           station                                    name  latitude  longitude  \
    0  USC00519397                    WAIKIKI 717.2, HI US   21.2716  -157.8168   
    1  USC00513117                    KANEOHE 838.1, HI US   21.4234  -157.8015   
    2  USC00514830  KUALOA RANCH HEADQUARTERS 886.9, HI US   21.5213  -157.8374   
    3  USC00517948                       PEARL CITY, HI US   21.3934  -157.9751   
    4  USC00518838              UPPER WAHIAWA 874.3, HI US   21.4992  -158.0111   
    
       elevation  
    0        3.0  
    1       14.6  
    2        7.0  
    3       11.9  
    4      306.6  



```python
#Check if there are any missing values in the dataframes:
print(hawaii_measurements.isnull().any())
```

    station    False
    date       False
    prcp        True
    tobs       False
    dtype: bool



```python
print(hawaii_stations.isnull().any())
```

    station      False
    name         False
    latitude     False
    longitude    False
    elevation    False
    dtype: bool



```python
# Drop the missing values from hawaii_measurements:
hawaii_measurements = hawaii_measurements.dropna()
```


```python
#Verify the data has been dropped:
hawaii_measurements.isnull().any()
```




    station    False
    date       False
    prcp       False
    tobs       False
    dtype: bool




```python
#Write new CSV files with the cleaned data:
hawaii_measurements.to_csv("resources/clean_hawaii_measurements.csv")
hawaii_stations.to_csv("resources/clean_hawaii_stations.csv")
```
