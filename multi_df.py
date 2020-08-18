#!/usr/bin/env python3.7.7
# -*- Coding: UTF-8 -*-

from helpers.nchlp import Nchlp
from helpers.timer import Timer
t = Timer()
from multiprocessing import Pool
from multiprocessing import freeze_support
from multiprocessing import cpu_count
from tqdm import tqdm

# Load df_in
df_in = Nchlp.read_csv('data/sample.csv')
# Create df with all lat/lons without duplicates
df_out = Nchlp.create_df(df_in)

def run_multiprocessing(func, i, n_processors):
    '''
    Run mutiple processors and pool the results together as list of tuples
    '''
    with Pool(processes=n_processors) as pool:
        return pool.map(func, i)

def loop(n):
    '''
    Tasks inside loop
    '''
    global df_in
    lat = df_out.iloc[n]['latitude']
    lon = df_out.iloc[n]['longitude']
    # Select rows by lat/lon
    df_select = Nchlp.select_df(df_in, lat, lon)
    # Pixel's calculus
    var_value = Nchlp.calculus(df_select)
    # Print control
    #print('{0}/{1}'.format(n,df_out.shape[0]))
    return lat, lon, var_value

def main():
    global df_out
    # Number of processors
    n_processors = cpu_count()
    # Pass the task function, followed by the parameters to processors
    x_ls = list(range(df_out.shape[0]))
    lst_var = tqdm(run_multiprocessing(loop, x_ls, n_processors))
    # Save pixel's values
    df_out = Nchlp.df_update(df_out, lst_var)

    # Save df
    Nchlp.df_to_csv(df_out, 'data/df_out.csv')
    # Save netCDF
    Nchlp.df_to_nc(df_out, 'data/map_out.nc')

if __name__ == "__main__":
    freeze_support()
    main()
