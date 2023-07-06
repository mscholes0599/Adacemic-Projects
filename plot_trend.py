def trend_plot(path, trend_data, p_data, depth_level, title):
    sig_trend = np.zeros((330, 360)) #np.zeros for historical data
    sig_trend[:,:] = np.nan
    notsig_trend = np.zeros((330, 360))
    notsig_trend[:,:] = np.nan
    trend_cube = iris.load_cube(path+trend_data)
    ps_cube = iris.load_cube(path+p_data)
    depths = trend_cube.coord('depth').points
    lats = trend_cube.coord('latitude').points
    lons = trend_cube.coord('longitude').points
    trend_cube = trend_cube[depth_level]
    ps_cube = ps_cube[depth_level]
    trend = trend_cube.data
    trend[trend == 0] = np.nan 
    ps = ps_cube.data

    #Find the significant values
    sig_ind = np.argwhere(ps<0.1)
    notsig_ind = np.argwhere(ps>=0.1)

    #modify format so can be set on the grid
    sigx_ind = sig_ind[:,0]
    sigy_ind = sig_ind[:,1]
    notsigx_ind = notsig_ind[:,0]
    notsigy_ind = notsig_ind[:,1]
    sig_trend[sigx_ind, sigy_ind] = trend[sigx_ind, sigy_ind]
    notsig_trend[notsigx_ind, notsigy_ind] = trend[notsigx_ind, notsigy_ind]

    #begin the plot
    X, Y = np.meshgrid(lons, lats)
    ax = plt.axes(projection=ccrs.PlateCarree())
    levels = np.linspace(-0.02, 0.02, 21)
    trend_plot = ax.contourf(X, Y, trend, levels = levels, alpha=1, extend = 'both', cmap = plt.cm.BrBG)
    sig = ax.contourf(X, Y, sig_trend, extend = 'both' , hatches=['', '..'],  alpha=0.25, cmap = plt.cm.BrBG)
    cbar1 = plt.colorbar(trend_plot, extend='both')
    
    cbar1.set_label('m/s')
    plt.title(str(title))
    ax.coastlines()
    plt.show()
