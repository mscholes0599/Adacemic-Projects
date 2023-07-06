def save_netcdf(filename, path, depth, lat, lon, standard_name, units):

    """
    A standard method to save netcdf files which are used regularly throughout the project. Make sure  to comply with the CF naming conventions to mantain consistency
    """
    fn = str(path)+str(filename)
    ncfile = nc4.Dataset(fn, mode='w', format='NETCDF4')

    lat_dim = ncfile.createDimension('lat', len(lat))     # latitude axis
    lon_dim = ncfile.createDimension('lon', len(lon))    # longitude axis
    depth_dim = ncfile.createDimension('depth', len(depth)) # unlimited axis (can be appended to).

    lats = ncfile.createVariable('lat', np.float32, ('lat',))
    lats.units = 'degrees_north'
    lats.long_name = 'latitude'
    lons = ncfile.createVariable('lon', np.float32, ('lon',))
    lons.units = 'degrees_east'
    lons.long_name = 'longitude'
    depths = ncfile.createVariable('depth', np.float64, ('depth',))
    depths.units = units
    depths.long_name = 'depth from surface'

    nc = ncfile.createVariable('sos_trend',np.float64,('depth','lat','lon')) # note: unlimited dimension is leftmost
    nc.units = units # degrees Kelvin
    nc.standard_name = standard_name # this is a CF standard name

    lats[:] = lat
    lons[:] = lon
    depths[:] = depth
    nc[:,:,:] = data  # Appends data along unlimited dimension
    print("completed", filename)
    ncfile.close()
