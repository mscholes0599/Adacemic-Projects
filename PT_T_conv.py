def prep2(thetafile, saltfile):
    rootgrp1 = nc4.Dataset(thetafile, 'r')
    rootgrp2 = nc4.Dataset(saltfile, 'r')

    #time           = rootgrp1.variables['time']
    lat            = rootgrp1.variables['latitude']
    lon            = rootgrp1.variables['longitude']
    pot_temp       = rootgrp1.variables['thetao'] #Kelvin
    salt           = rootgrp2.variables['so'] #PSU
    depth          = rootgrp2.variables['lev'] #metres
    lon2           = rootgrp2.variables['i']
    lat2           = rootgrp2.variables['j']
    depth          = depth[::2] #Remove some of the levels to speed up the code

    #cant do all times at once so loop through each month
    for i in range(420):
        print('Calculating ',i, 'out of 419')

        #shape (75, 330, 360)
        my_salt = salt[i,:,:,:]
        my_pt = pot_temp[i,:,:,:]

        #Squeeze the data to turn into an array
        my_pt = np.squeeze(my_pt)
        my_salt = np.squeeze(my_salt)
        lat = np.squeeze(lat)
        lon = np.squeeze(lon)
       
        #Historical dataset has units of Kelvin so convert to celsius
        #pot_temp = np.subtract(pot_temp, 273.15)

        #Convert depth into a grid of depths and latitudes
        depth          = np.meshgrid(depth, lat)[0].T 

        #Uncomment for historical data, this is due to different formatting with CMIP
        my_lat = lat.reshape(len(depth[0,:]))

        #Calculate the pressure to convert PT to T
        pressure_array = sw.eos80.pres(depth, my_lat) 

        #Remove from latitude grid such that 1D array
        pressure_array = pressure_array.flatten('F')[0:75] #42 pressure levels in historical and 75 for cmip
        
        #Return pressure into a 3D grid
        pressure       = np.meshgrid(lat2, pressure_array, lon2)[0] #put into a grid

        #Calculate the temperature 
        t1 = time.time()
        temp            = sw.eos80.temp(my_salt, my_pt, pressure, 0)
        t2 = time.time()
        t = t2-t1

        #Redefine the depths to standard format
        depth          = rootgrp1.variables['lev']
        depth          = np.squeeze(depth)

        #Save this temperature cube
        save_netcdf('/storage/teaching/MPhysProject/s1748379/mphys/spp558/temp_files/temp'+str(i)+'_mean.nc', temp, depth, np.squeeze(lat2), np.squeeze(lon2), 'temperature', 'celsius')
