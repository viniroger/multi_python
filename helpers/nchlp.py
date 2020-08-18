#!/usr/bin/env python3.7.7
# -*- Coding: UTF-8 -*-

'''
Functions to work with dataframes
author: Vinicius Roggério da Rocha
e-mail: viniroger@yahoo.com.br
version: 0.0.1
date: 2020-08-14
'''

import pandas as pd
import xarray as xr

class Nchlp():
    '''
    Functions to work with dataframes
    '''

    @staticmethod
    def read_csv(filename):
        '''
        Read CSV by file name
        '''
        df = pd.read_csv(filename)
        return df

    @staticmethod
    def create_df(df):
        '''
        Create df with latitude and longitude columns
        '''
        df = df[['latitude', 'longitude']]
        df = df.drop_duplicates(subset=['latitude', 'longitude']).reset_index(drop=True)
        df['cpd'] = None
        return df

    @staticmethod
    def select_df(df, lat, lon):
        '''
        Select df rows based on latitude and longitude values
        '''
        return df.loc[(df['latitude'] == lat) & (df['longitude'] == lon)]

    @staticmethod
    def calculus(df):
        '''
        Calculus
        '''
        var_value = df['value'].values.mean()
        return var_value

    @staticmethod
    def df_update(df, data):
        '''
        Update df - insert value at lat/lon row from df
        '''
        df = pd.DataFrame(data, columns=['latitude', 'longitude', 'value'])
        return df

    @staticmethod
    def df_to_csv(df, filename):
        '''
        Save DF into CSV
        '''
        df.to_csv(filename, index=False)

    @staticmethod
    def df_to_nc(df, filename):
        '''
        Convert dataframe to netcdf file
        '''
        ds = df.set_index(['latitude', 'longitude']).to_xarray()
        ds.to_netcdf(filename)
