# -*- coding: utf-8 -*-
"""
@author: Jellen Vermeir
"""

import datetime
import dateutil.parser
import pandas as pd
import numpy as np
import json

###########################
### Serialization Class ###
###########################
class EssentialJSONSerializer:
    
    # Custom 'language independent datatypes'
    custom_types = ['datetime', 'timeseries', 'timeseries_n_dim', 'series', 'dataframe', 'matrix']
   
    @classmethod
    def python_to_dict(cls, to_convert):
        
        
        if to_convert is None:
            return to_convert
        # convert python datetime to datetime dict
        if cls.datetime_type_check(to_convert):
            to_convert = cls.datetime_to_dict(to_convert, custom_type_name = 'datetime')
                
        # convert python series to timeseries dict
        elif cls.timeseries_type_check(to_convert):
            to_convert = cls.timeseries_to_dict(to_convert, custom_type_name = 'timeseries')
            
        # convert python dataframe to timeseries_n_dim dict
        elif cls.timeseries_n_dim_type_check(to_convert):
            to_convert = cls.timeseries_n_dim_to_dict(to_convert, custom_type_name = 'timeseries_n_dim')
            
        # convert python series to series dict
        elif cls.series_type_check(to_convert):
            to_convert = cls.series_to_dict(to_convert, custom_type_name = 'series')
            
        # convert python dataframe to dataframe dict
        elif cls.dataframe_type_check(to_convert):
            to_convert = cls.dataframe_to_dict(to_convert, custom_type_name = 'dataframe')
        
        # convert pythonn numpy array to matrix dict
        elif cls.matrix_type_check(to_convert):
            to_convert = cls.matrix_to_dict(to_convert, custom_type_name = 'matrix')
            
        elif isinstance(to_convert, dict) and len(to_convert) > 0:
            for k,v in to_convert.items():
                to_convert[k] = cls.python_to_dict(v) 
                
        # to dict
        return(to_convert)
        
    @classmethod
    def python_to_json(cls, to_convert):
        return(json.dumps(cls.python_to_dict(to_convert)).replace('NaN', 'null'))
        
    
    @classmethod
    def python_from_dict(cls, to_convert):
        
        if to_convert is None:
            return(to_convert)
            
        # convert datetime dict to python datetime
        if cls.type_check_from_dict(to_convert, 'datetime'):
            to_convert = cls.datetime_from_dict(to_convert)
            
        # convert timeseries dict to python series
        elif cls.type_check_from_dict(to_convert, 'timeseries'):
            to_convert = cls.timeseries_from_dict(to_convert)
            
        # convert timeseries_n_dim dict to python dataframe
        elif cls.type_check_from_dict(to_convert, 'timeseries_n_dim'):
            to_convert = cls.timeseries_n_dim_from_dict(to_convert)
            
        # convert series dict to python series
        elif cls.type_check_from_dict(to_convert, 'series'):
            to_convert = cls.series_from_dict(to_convert)
            
        # convert dataframe dict to python dataframe
        elif cls.type_check_from_dict(to_convert, 'dataframe'):
            to_convert = cls.dataframe_from_dict(to_convert)
            
        # convert matrix dict to python numpy array
        elif cls.type_check_from_dict(to_convert, 'matrix'):
            to_convert = cls.matrix_from_dict(to_convert)
            
        elif isinstance(to_convert, dict) and len(to_convert) > 0:
            for k,v in to_convert.items():
                to_convert[k] = cls.python_from_dict(v)
        
        return(to_convert)
    
        
    @classmethod
    def python_from_json(cls, to_convert):
        return(cls.python_from_dict(json.loads(to_convert)))

    # Check for custom type
    @classmethod
    def type_check_from_dict(cls, input_values, custom_type_name):
        return(isinstance(input_values, dict) and input_values.get('_type') == custom_type_name)
    
    #####################
    ### datetime ########
    #####################
    # check language specific datetime format
    @classmethod
    def datetime_type_check(cls, input_values):
        return(isinstance(input_values, datetime.datetime))
    
    # Convert lanugage specific datetime object to datetime dict
    @classmethod
    def datetime_to_dict(cls, datetime_python, custom_type_name):
        datetime_dict = {
                         '_type': custom_type_name, 
                         '_data': datetime_python.isoformat()
                        }
        return(datetime_dict)
            
    # convert datetime dict to language specific datetime object
    @classmethod
    def datetime_from_dict(cls, input_values):
        return(dateutil.parser.parse(input_values['_data']))
    
    
    ####################
    ### Timeseries   ###
    ####################
    # check language specific timeseries format
    @classmethod
    def timeseries_type_check(cls, input_values):
        return(isinstance(input_values, pd.Series) and isinstance(input_values.index, pd.DatetimeIndex))
    
    # Convert lanugage specific timseries object to timeseries dict
    @classmethod
    def timeseries_to_dict(cls, timeseries_python, custom_type_name):
        
        series_name = timeseries_python.name if timeseries_python.name is not None else 'values'
        values_list = timeseries_python.values.tolist()
        timestamps_list = list(map(lambda x: x.isoformat(), timeseries_python.index.tolist()))
        timeseries_dict = {
                            '_type': custom_type_name, 
                            '_data'      : {
                                            '_timestamps' : timestamps_list,
                                             series_name : values_list 
                                           },
                          }
        return(timeseries_dict)
            
    # convert timeseries dict to language specific timeseries object
    @classmethod
    def timeseries_from_dict(cls, input_values):
        
        data_dict     = input_values['_data']
        series_index  = pd.DatetimeIndex(list(map(lambda x: dateutil.parser.parse(x), data_dict['_timestamps'])))
        
        for dict_key in data_dict.keys():
            if dict_key is not '_timestamps':
                series_values = data_dict[dict_key]
                series_output = pd.Series(series_values, index=series_index, name = dict_key)
        
        return(series_output)
    
    
    ########################
    ### timeseries_n_dim ###
    ########################
    
     # check language specific timeseries_n_dim format
    @classmethod
    def timeseries_n_dim_type_check(cls, input_values):
        return(isinstance(input_values, pd.DataFrame) and isinstance(input_values.index, pd.DatetimeIndex))
    
    # Convert lanugage specific timseries_n_dim object to timeseries_n_dim dict
    @classmethod
    def timeseries_n_dim_to_dict(cls, timeseries_n_dim_python, custom_type_name):
        timestamps_list   = list(map(lambda x: x.isoformat(), timeseries_n_dim_python.index.tolist()))    
        timeseries_n_dim_dict = { '_type': custom_type_name,
                                  '_data'      : {
                                                  '_timestamps' : timestamps_list
                                                 }
                                }
                              
        for df_key in timeseries_n_dim_python.columns:
            timeseries_n_dim_dict['_data'][df_key] = timeseries_n_dim_python[df_key].values.tolist()
            
        return(timeseries_n_dim_dict)
    
    # convert timeseries_n_dim dict to language specific timeseries_n_dim object
    @classmethod
    def timeseries_n_dim_from_dict(cls, input_values):
        
        data_dict = input_values['_data']
        dataframe_index = pd.DatetimeIndex(list(map(lambda x: dateutil.parser.parse(x), data_dict['_timestamps'])))
        
        data_dict.pop('_timestamps')
        dataframe_output = pd.DataFrame(data_dict, index=dataframe_index)
        
        return(dataframe_output)
        
    
    ####################
    ### series #########
    ####################
    # check language specific series format
    @classmethod
    def series_type_check(cls, input_values):
        return(isinstance(input_values, pd.Series) and not isinstance(input_values.index, pd.DatetimeIndex))
    
    # Convert lanugage specific series object to series dict
    @classmethod
    def series_to_dict(cls, series_python, custom_type_name):
        
        series_name = series_python.name if series_python.name is not None else 'values'
        values_list = series_python.values.tolist()
        index_list  = series_python.index.tolist()
        series_dict = {
                        '_type': custom_type_name, 
                        '_data'      : {
                                        '_index' : index_list,
                                         series_name : values_list 
                                       },
                      }
        return(series_dict)

    # convert series dict to language specific series object
    @classmethod
    def series_from_dict(cls, input_values):
        
        data_dict = input_values['_data']
        series_index = data_dict['_index']
        
        for dict_key in data_dict.keys():
            if dict_key is not '_index':
                series_values = data_dict[dict_key]
                series_output = pd.Series(series_values, index=series_index, name = dict_key)
                
        return(series_output)
    
    
    #####################
    ### dataframe #######
    #####################
    
    # check language specific dataframe format
    @classmethod
    def dataframe_type_check(cls, input_values):
        return(isinstance(input_values, pd.DataFrame) and not isinstance(input_values.index, pd.DatetimeIndex))
    
    # Convert lanugage specific dataframe object to dataframe dict
    @classmethod
    def dataframe_to_dict(cls, dataframe_python, custom_type_name):
        index_list        = dataframe_python.index.tolist()
        dataframe_dict = { 
                            '_type': custom_type_name,
                            '_data'      : {
                                            '_index' : index_list
                                           }
                         }
                              
        for df_key in dataframe_python.columns:
            dataframe_dict['_data'][df_key] = dataframe_python[df_key].values.tolist()
            
        return(dataframe_dict)
    
    # convert dataframe dict to language specific dataframe object
    @classmethod
    def dataframe_from_dict(cls, input_values):
        
        data_dict       = input_values['_data']
        dataframe_index = data_dict['_index']
        
        data_dict.pop('_index')
        dataframe_output = pd.DataFrame(data_dict, index=dataframe_index)
        
        return(dataframe_output)
    
    
    
    ####################
    ### matrix #########
    ####################
    
    # check language specific matrix format
    @classmethod
    def matrix_type_check(cls, input_values):
        return(isinstance(input_values, np.ndarray))
    
    # Convert lanugage specific matrix object to matrix dict
    @classmethod
    def matrix_to_dict(cls, matrix_python, custom_type_name):
        matrix_values = matrix_python.tolist()
        matrix_dict   = { 
                          '_type': custom_type_name,
                          '_data': matrix_values
                        }
            
        return(matrix_dict)
    
    # convert matrix dict to language specific matrix object
    @classmethod
    def matrix_from_dict(cls, input_values):
        return(np.array(input_values['_data']))