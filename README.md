
# EssentialJSONSerializer (Python package)
The intention of the package fuctionality is to (de)serialize language specific complex objects towards generic 
JSON-datatype objects. The JSON conversion allows for flexible cross language communication when the package is implemented
across different languages. This package provides a Python implementation of the (de)serialization functionality.

**Installation**:

`pip install git+https://github.com/VermeirJellen/essentialjsonserializer_python.git`

JSON (de)serialization of complex Python-objects.
--------------------------------------------

Currently, 6 generic complex JSON-datatypes are provided. Corresponding Python-mappings are defined as follows:

-   JSON **datetime** - maps to Python `datetime.datetime` objects
-   JSON **timeseries** - maps to Python `pandas.Series` objects (with `pandas.DatetimeIndex` index)
-   JSON **timeseries\_n\_dim** - maps to Python n-dimensional `pandas.DataFrame` objects (n &gt; 1) (with `pandas.DatetimeIndex` index)
-   JSON **series** - maps to Python 1-dimensional `pandas.Series` objects
-   JSON **dataframe** - maps to Python n-dimensional `pandas.DataFrame` objects (n &gt; 1)
-   JSON **matrix** - maps to Python `numpy.array` objects

The package provides the user with the `EssentialJSONSerializer` class. Following methods are provided:

-   `python_to_dict`: Convert complex Python structures to a generic `dict` structure.
-   `python_to_json`: Convert complex Python structures to a generic datatype JSON structure.
-   `python_from_list`: Convert generic `dict` structure to complex Python-specific objects.
-   `python_from_json`: Convert generic datatype JSON structure to complex Python-specific objects.

Examples
--------

#### **EssentialJSONSerializer Object Construction**


```python
import pytz
import datetime
import pandas as pd
import numpy as np
import essentialjsonserializer
essential_serializer = essentialjsonserializer.EssentialJSONSerializer
essential_serializer
```




    essentialjsonserializer.essentialjsonserializer.EssentialJSONSerializer



#### **list**

Serialize:


```python
list_input = [[1, 2, 3, 4], [5, 6, 7, 8]]
list_json  = essential_serializer.python_to_json(list_input)

list_json
```




    '[[1, 2, 3, 4], [5, 6, 7, 8]]'



Deserialize:


```python
list_revert = essential_serializer.python_from_json(list_json)
list_revert
```




    [[1, 2, 3, 4], [5, 6, 7, 8]]



#### **datetime**

Serialize:


```python
# custom datastructure: datetime
datetime_input         = datetime.datetime(2017, 1, 1, 0, 0, 0, 0, pytz.UTC)
datetime_json          = essential_serializer.python_to_json(datetime_input)
datetime_json
```




    '{"_type": "datetime", "_data": "2017-01-01T00:00:00+00:00"}'



Deserialize:


```python
datetime_revert        = essential_serializer.python_from_json(datetime_json)
datetime_revert
```




    datetime.datetime(2017, 1, 1, 0, 0, tzinfo=tzutc())



#### **timeseries**

Serialize:


```python
timeseries_input       = pd.Series([0, 1, 2, 3, np.nan], \
                                   index=pd.DatetimeIndex(['2014-07-04', '2014-08-04','2015-07-04', '2015-08-04', '2015-08-05']), name='series_name')
timeseries_json        = essential_serializer.python_to_json(timeseries_input)
timeseries_json
```




    '{"_type": "timeseries", "_data": {"_timestamps": ["2014-07-04T00:00:00", "2014-08-04T00:00:00", "2015-07-04T00:00:00", "2015-08-04T00:00:00", "2015-08-05T00:00:00"], "series_name": [0.0, 1.0, 2.0, 3.0, null]}}'



Deserialize:


```python
timeseries_revert      = essential_serializer.python_from_json(timeseries_json)
timeseries_revert
```




    2014-07-04    0.0
    2014-08-04    1.0
    2015-07-04    2.0
    2015-08-04    3.0
    2015-08-05    NaN
    Name: series_name, dtype: float64



#### **timeseries_n_dim**

Serialize:


```python
timeseries_n_dim_input  = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]}, index=pd.DatetimeIndex(['2014-07-04', '2014-08-04','2015-07-04']))
timeseries_n_dim_json   = essential_serializer.python_to_json(timeseries_n_dim_input)
timeseries_n_dim_json
```




    '{"_type": "timeseries_n_dim", "_data": {"_timestamps": ["2014-07-04T00:00:00", "2014-08-04T00:00:00", "2015-07-04T00:00:00"], "col1": [1, 2, 3], "col2": [4, 5, 6]}}'



Deserialize:


```python
timeseries_n_dim_revert = essential_serializer.python_from_json(timeseries_n_dim_json)
timeseries_n_dim_revert
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
      <th>col1</th>
      <th>col2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>2014-07-04</th>
      <td>1</td>
      <td>4</td>
    </tr>
    <tr>
      <th>2014-08-04</th>
      <td>2</td>
      <td>5</td>
    </tr>
    <tr>
      <th>2015-07-04</th>
      <td>3</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



#### **series**

Serialize:


```python
series_input           = pd.Series([5, 6, 7, 8], name='series_name')
series_json            = essential_serializer.python_to_json(series_input)
series_json
```




    '{"_type": "series", "_data": {"_index": [0, 1, 2, 3], "series_name": [5, 6, 7, 8]}}'



Deserialize:


```python
series_revert          = essential_serializer.python_from_json(series_json)
series_revert
```




    0    5
    1    6
    2    7
    3    8
    Name: series_name, dtype: int64



#### **dataframe**

Serialize:


```python
dataframe_input        = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]}, index=['n1', 'n2', 'n3'])
dataframe_json         = essential_serializer.python_to_json(dataframe_input)
dataframe_json
```




    '{"_type": "dataframe", "_data": {"_index": ["n1", "n2", "n3"], "col1": [1, 2, 3], "col2": [4, 5, 6]}}'



Deserialize:


```python
dataframe_revert       = essential_serializer.python_from_json(dataframe_json)
dataframe_revert
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
      <th>col1</th>
      <th>col2</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>n1</th>
      <td>1</td>
      <td>4</td>
    </tr>
    <tr>
      <th>n2</th>
      <td>2</td>
      <td>5</td>
    </tr>
    <tr>
      <th>n3</th>
      <td>3</td>
      <td>6</td>
    </tr>
  </tbody>
</table>
</div>



#### **matrix**

Serialize:


```python
matrix_input  = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
matrix_json   = essential_serializer.python_to_json(matrix_input)
matrix_json
```




    '{"_type": "matrix", "_data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}'



Deserialize:


```python
matrix_revert = essential_serializer.python_from_json(matrix_json)
matrix_revert
```




    array([[1, 2, 3],
           [4, 5, 6],
           [7, 8, 9]])



#### **nested structure**

Serialize:


```python
python_complex = {
                  'list_input': [[1, 2, 3, 4], [5, 6, 7, 8]],
                  'datetime_input': datetime_input,
                  'timeseries_input': timeseries_input,
                  'timeseries_n_dim_input': timeseries_n_dim_input,
                  'series_input': series_input,
                  'dataframe_input': dataframe_input,
                  'matrix_input': matrix_input
              }

output_dict           = essentialjsonserializer.EssentialJSONSerializer.python_to_dict(python_complex)
output_json           = essentialjsonserializer.EssentialJSONSerializer.python_to_json(python_complex)
output_json
```




    '{"list_input": [[1, 2, 3, 4], [5, 6, 7, 8]], "datetime_input": {"_type": "datetime", "_data": "2017-01-01T00:00:00+00:00"}, "timeseries_input": {"_type": "timeseries", "_data": {"_timestamps": ["2014-07-04T00:00:00", "2014-08-04T00:00:00", "2015-07-04T00:00:00", "2015-08-04T00:00:00", "2015-08-05T00:00:00"], "series_name": [0.0, 1.0, 2.0, 3.0, null]}}, "timeseries_n_dim_input": {"_type": "timeseries_n_dim", "_data": {"_timestamps": ["2014-07-04T00:00:00", "2014-08-04T00:00:00", "2015-07-04T00:00:00"], "col1": [1, 2, 3], "col2": [4, 5, 6]}}, "series_input": {"_type": "series", "_data": {"_index": [0, 1, 2, 3], "series_name": [5, 6, 7, 8]}}, "dataframe_input": {"_type": "dataframe", "_data": {"_index": ["n1", "n2", "n3"], "col1": [1, 2, 3], "col2": [4, 5, 6]}}, "matrix_input": {"_type": "matrix", "_data": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]}}'



Deserialize:


```python
python_complex_revert = essentialjsonserializer.EssentialJSONSerializer.python_from_dict(output_dict)
python_complex_revert = essentialjsonserializer.EssentialJSONSerializer.python_from_json(output_json)
python_complex_revert
```




    {'list_input': [[1, 2, 3, 4], [5, 6, 7, 8]],
     'datetime_input': datetime.datetime(2017, 1, 1, 0, 0, tzinfo=tzutc()),
     'timeseries_input': 2014-07-04    0.0
     2014-08-04    1.0
     2015-07-04    2.0
     2015-08-04    3.0
     2015-08-05    NaN
     Name: series_name, dtype: float64,
     'timeseries_n_dim_input':             col1  col2
     2014-07-04     1     4
     2014-08-04     2     5
     2015-07-04     3     6,
     'series_input': 0    5
     1    6
     2    7
     3    8
     Name: series_name, dtype: int64,
     'dataframe_input':     col1  col2
     n1     1     4
     n2     2     5
     n3     3     6,
     'matrix_input': array([[1, 2, 3],
            [4, 5, 6],
            [7, 8, 9]])}



## Donations

If you find this software useful and/or you would like to see additional extensions, feel free to donate some btc:

 - BTC: 3NmxUnuK8ZqAszzFzcpBerKsy4ajQpb8mi
 
## Licensing

Copyright 2019 Essential Data Science Consulting ltd. ([EssentialDataScience.com](http://essentialdatascience.com "EssentialDataScience") / jellenvermeir@essentialdatascience.com).
This software is copyrighted under the MIT license: View added [LICENSE](./LICENSE) file.
