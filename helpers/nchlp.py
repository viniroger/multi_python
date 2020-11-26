#!/usr/bin/env python3.7.7
# -*- Coding: UTF-8 -*-

'''
Functions to work with dataframes
author: Vinicius Roggério da Rocha
e-mail: viniroger@yahoo.com.br
version: 0.0.1
date: 2020-08-14
'''

from datetime import datetime
import time
import numpy as np
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

    @staticmethod
    def nc_to_array(filename, var_name):
        '''
        Convert dataset from netCDF to numpy array
        '''
        dataset = xr.open_dataset(filename)
        return dataset[var_name]

    @staticmethod
    def meshgrid(dataset):
        '''
        Create array of indexes
        '''
        lat, lon = np.meshgrid(dataset['latitude'], dataset['longitude'])
        # Transpose to get rows with same value of latitude
        return lat.transpose(), lon.transpose()

    @staticmethod
    def get_datetime(filename):
        '''
        Get date and time info from filename
        '''
        date_str = filename.split('/')[-1].split('_')[-1]
        strptime_object = time.strptime(date_str[:], 'sat%j%Y.%H%M.nc')
        dt = datetime.fromtimestamp(time.mktime(strptime_object))
        day = dt.strftime("%Y-%m-%d")
        return dt, day

    @staticmethod
    def calc_astro(ts, lat, lon):
        '''
        Calculate earth-sun distance, zenith angle and TOA
        '''
        #ts = ts - timedelta(hours=3)
        doy = ts.timetuple().tm_yday
        hour = ts.hour
        minute = 60*hour + ts.minute
        pi = np.pi

        # Day angle (in radians)
        day_angle = ((360.*(doy-1))/365.15)*pi/180.
        # Solar declination (in radians)
        dec = (0.006918 - 0.399912 * np.cos(day_angle)
            + 0.070257 * np.sin(day_angle) - 0.006758 * np.cos(2 * day_angle)
            + 0.000907 * np.sin(2 * day_angle) - 0.002697 * np.cos(3 * day_angle)
            + 0.001480 * np.sin(3 * day_angle))

        # Earth-Sun distance from day of year
        d_astro = (1.00011 + 0.034221 * np.cos(day_angle)
            + 0.00128 * np.sin(day_angle) + 0.000719 * np.cos(2 * day_angle)
            + 0.000077 * np.sin(2 * day_angle))

        # Time Equation (in minutes)
        eqtime = (0.000075 + 0.001868 * np.cos(day_angle)
            - 0.032077 * np.sin(day_angle) - 0.014615 * np.cos(2 * day_angle)
            - 0.040849 * np.sin(2 * day_angle)) * ((180 * 4)/(pi))
        # Total time translated (solar time, in hours)
        tcorr = (minute/60. + lon/15. + eqtime/60.)
        # Hour angle (in radians)
        H0 = ((12. - tcorr) * 15.) * pi/180.

        # Zenital angle cosine
        cosZ = ((np.sin(dec) * np.sin(lat*pi/180.))
            + (np.cos(dec) * np.cos(lat*pi/180.) * np.cos(H0)))
        # Zenital angle (in degrees)
        Z = np.arccos(cosZ)*180./pi

        # Calculate Top Of Atmosphere Irradiance (TOA)
        toa = 1367 * d_astro * cosZ

        return Z, cosZ, toa

    @staticmethod
    def conditions(Z, data_array):
        '''
        Replace points where condition is not satisfied by nan
        '''
        data_out = data_array.where((Z < 80) & (data_array != -999))
        return data_out

    @staticmethod
    def calc(data_array, nd_array):
        '''
        Multiply numpy.ndarray and xarray...DataArray
        '''
        result = data_array * nd_array
        return result

    @staticmethod
    def xr_to_nc(dataset, filename):
        '''
        Save xarray/dataset to netCDF file
        '''
        dataset.to_netcdf(filename, unlimited_dims={'time':True}, format='NETCDF4_CLASSIC')
