def remove_seasonality(cube, remainder, my_time, months, years):
    """
    Before calculating the linear trend in the sos data, one must remove the seasonality implementing lag difference
    Take in the sos data as a master cube and input a remaider list, calculated in trend, 
    my_time which is an integer list of all months, months which is a list from 0-11 to represent the months
    on an annual cycle. Finally pass through the number of years available in the cube
    """

    #split into months
    month_cubes = []
    for month in months:
        ind = np.where(np.array(remainder) == month)
        month_list = my_time[ind]
        month_cube = cube.extract(iris.Constraint(time=month_list))
        month_cubes.append(month_cube)
    
    #calc monthly means
    mean_cubes = []
    for month_cube in month_cubes:
        mean_cube = month_cube.collapsed('time', iris.analysis.MEAN)
        mean_cubes.append(mean_cube)
    
    #remove seasonality
    no_sn_list = []
    for month in months:
        data = month_cubes[month]
        mean = mean_cubes[month]
        no_sn = data-mean
        no_sn_list.append(no_sn)

    #reorder into months
    reorder_list = []
    for i in range(years):
        for month in months:
            reorder = no_sn_list[month][i]
            reorder_list.append(reorder)

    cube_list = iris.cube.CubeList(reorder_list)
    no_sn_cube = cube_list.merge_cube()
    iris.save(no_sn_cube, '/storage/teaching/MPhysProject/s1748379/mphys/spp558/no_seasonality.nc')
    #no_sn_data = no_sn_cube.data
    #depths = no_sn_cube.coord('depth').points
    #lats = no_sn_cube.coord('latitude').points
    #lons = no_sn_cube.coord('longitude').points
    #save_netcdf('no_seasonality.nc', no_sn_data, depths, lats, lons, 'speed_of_sound_in_sea_water', 'm/s')
    print('seasonality removed')

def trend():
    """
    uncomment first section if needing to remove the seasonality of the cube
    trend calculated with p-values
    trend can also be calculated with weights, which utilises np.polyfit
    """
    """
    cube = iris.load_cube('/storage/teaching/MPhysProject/s1748379/mphys/spp558/master_sos.nc')
    my_time = np.linspace(0, 419, 420)
    remainder = []
    months = [0,1,2,3,4,5,6,7,8,9,10,11]
    for t in my_time:
        rem = t%12
        remainder.append(rem)
        
    remove_seasonality(cube, remainder, my_time, months, 35)
    exit()
    """
    cube = iris.load_cube('/storage/teaching/MPhysProject/s1748379/mphys/spp558/no_seasonality.nc')
    depths = cube.coord('depth').points
    lats = cube.coord('latitude').points
    lons = cube.coord('longitude').points
    trend = np.zeros((42, 330, 360))
    ps = np.zeros((42, 330, 360))
    #trend = np.zeros((42, 173, 360))
    #ps = np.zeros((42, 173, 360))

    for d in range(len(depths)):
        print('calculating ', d,'/75')
        vals = cube.extract(iris.Constraint(depth=depths[d])).data
        slope_arr = np.zeros(vals.shape[1:])
        p_arr = np.zeros(vals.shape[1:])
        for lat in range(len(lats)):
            for lon in range(len(lons)):
                slope, intercept, r, p, se = linregress(my_time, vals[:,lat,lon])
                slope_arr[lat,lon] = slope
                p_arr[lat,lon] = p
        slope_arr[slope_arr < -100] = np.nan
        slope_arr[slope_arr > 100] = np.nan
        p_arr[p_arr == 1] = np.nan
        p_arr[slope_arr > 100] = np.nan
        trend[d, :, :] = slope_arr
        ps[d,:,:] = p_arr
        #print(np.nanmean(trend))
        #print(np.nanmax(trend))
        #print(np.nanmin(trend))
        #print(np.nanmedian(trend))
    save_netcdf('/storage/teaching/MPhysProject/s1748379/mphys/spp558/all_trend2.nc', trend, depths, lats, lons, 'sos_trend', 'm/s per month')
    save_netcdf('/storage/teaching/MPhysProject/s1748379/mphys/spp558/all_ps.nc', ps, depths, lats, lons, 'sos_p_value', 'm/s per month')
