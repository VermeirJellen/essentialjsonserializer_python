# -*- coding: utf-8 -*-
"""
@author: Jellen Vermeir
"""
import pytz
import datetime
import pandas as pd
import numpy as np

import os
import essentialjsonserializer
essential_serializer = essentialjsonserializer.EssentialJSONSerializer

# custom datastructure: datetime
datetime_input         = datetime.datetime(2017, 1, 1, 0, 0, 0, 0, pytz.UTC)
datetime_json          = essential_serializer.python_to_json(datetime_input)
datetime_revert        = essential_serializer.python_from_json(datetime_json)

# custom datastructure: timeseries
timeseries_input       = pd.Series([0, 1, 2, 3, np.nan], \
                                   index=pd.DatetimeIndex(['2014-07-04', '2014-08-04','2015-07-04', '2015-08-04', '2015-08-05']), name='series_name')
timeseries_json        = essential_serializer.python_to_json(timeseries_input)
timeseries_revert      = essential_serializer.python_from_json(timeseries_json)

# custom datastructure: timeseries_n_dim
timeseries_n_dim_input  = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]}, index=pd.DatetimeIndex(['2014-07-04', '2014-08-04','2015-07-04']))
timeseries_n_dim_json   = essential_serializer.python_to_json(timeseries_n_dim_input)
timeseries_n_dim_revert = essential_serializer.python_from_json(timeseries_n_dim_json)

# custom datastructure: series
series_input           = pd.Series([5, 6, 7, 8], name='series_name')
series_json            = essential_serializer.python_to_json(series_input)
series_revert          = essential_serializer.python_from_json(series_json)

# custom datastructure: dataframe
dataframe_input        = pd.DataFrame({'col1': [1, 2, 3], 'col2': [4, 5, 6]}, index=['n1', 'n2', 'n3'])
dataframe_json         = essential_serializer.python_to_json(dataframe_input)
dataframe_revert       = essential_serializer.python_from_json(dataframe_json)

#  
matrix_input  = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
matrix_json   = essential_serializer.python_to_json(matrix_input)
matrix_revert = essential_serializer.python_from_json(matrix_json)

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

python_complex_revert = essentialjsonserializer.EssentialJSONSerializer.python_from_dict(output_dict)
python_complex_revert = essentialjsonserializer.EssentialJSONSerializer.python_from_json(output_json)