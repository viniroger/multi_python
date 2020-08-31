#!/usr/bin/env python3.7.7
# -*- Coding: UTF-8 -*-

from helpers.nchlp import Nchlp
from helpers.timer import Timer
t = Timer()

# Load netCDF file
filename = 'data/sat0012016.1500.nc'
dataset = Nchlp.nc_to_array(filename, 'imagem_vi')
# Create index matrix
lat, lon = Nchlp.meshgrid(dataset)

# Get time information by file name
timestamp, day = Nchlp.get_datetime(filename)
# Perform calculation for all points (using lat / lon)
Z, cosZ, toa = Nchlp.calc_astro(timestamp, lat, lon)

# Check points that meet condition
data_clean = Nchlp.conditions(Z, dataset)
# Perform calculation for all points (using dataset tb)
data_out = Nchlp.calc(data_clean, cosZ)
# Save final file
Nchlp.xr_to_nc(data_out, 'data/output.nc')
