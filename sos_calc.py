"""
Prepare the variables for calculation
"""

rootgrp = nc4.Dataset(inputFile, 'r')
#print(rootgrp.variables)

lat            = rootgrp.variables['lat']
lon            = rootgrp.variables['lon']
depth          = rootgrp.variables['depth'] #metres
pot_temp       = rootgrp.variables['temperature'] #Kelvin
salt           = rootgrp.variables['salinity'] #PSU
T_unc          = rootgrp.variables['temperature_uncertainty']
S_unc          = rootgrp.variables['salinity_uncertainty']
pot_temp = np.squeeze(pot_temp); salt = np.squeeze(salt); lat = np.squeeze(lat); lon = np.squeeze(lon)
T_unc = np.squeeze(T_unc); S_unc = np.squeeze(S_unc)#; D_unc = np.squeeze(D_unc);
pot_temp = np.subtract(pot_temp, 273.15)

depth          = np.meshgrid(depth, lat)[0].T #gives a matrix of x=173 (lat) and y=42 (depth)
pressure_array = sw.eos80.pres(depth, lat) #used to calculate temperature

pressure_array = pressure_array.flatten('F')[0:42]
pressure       = np.meshgrid(lat, pressure_array, lon)[0] #put into a grid

temp           = sw.eos80.temp(salt, pot_temp, pressure, 0)
depth          = rootgrp.variables['depth']
depth          = np.squeeze(depth)

#For plotting purposes
temp = ma.masked_where(temp<-100, temp)
pot_temp = ma.masked_where(pot_temp<-100, pot_temp)
T_unc = ma.masked_where(T_unc<-100, T_unc)
S_unc = ma.masked_where(S_unc<-100, S_unc)
D_unc = np.array([5.02375, 5.03415, 5.0491, 5.07065 ,5.10165, 5.14615, 5.2101, 5.3021, 5.4342,5.6238,5.8956,6.28485,6.84115, \
7.6337, 8.7585,10.3454,12.56605,15.6384,19.8226,25.40065,32.62965,41.6625,52.45035,64.6604,77.66965,90.6679,102.848,113.5934,122.57935, \
129.763, 135.30165,139.45375,142.50085,144.70265,146.27575,147.3904,148.1759,148.7268,149.113,149.382,149.5698,149.7007])


depth3d = np.zeros((len(depth),len(lat),len(lon)))
for ii in np.arange(len(lat)):
    for jj in np.arange(len(lon)):
        depth3d[:,ii,jj] = depth[:]

depth3d_unc = np.zeros((len(depth),len(lat),len(lon)))
for ii in np.arange(len(lat)):
    for jj in np.arange(len(lon)):
        depth3d_unc[:,ii,jj] = D_unc[:]

tsquared     = np.multiply(temp,temp)
tcubed       = np.multiply(temp,tsquared)
depthsquared = np.multiply(depth3d,depth3d)
depthcubed   = np.multiply(depth3d,depthsquared)
saltminus35  = np.subtract(salt,35)
s35squared   = np.multiply(saltminus35,saltminus35)
T_uncsquared = np.multiply(T_unc,T_unc)
S_uncsquared = np.multiply(S_unc,S_unc)
D_uncsquared = np.multiply(depth3d_unc,depth3d_unc)

m1 = 1448.96
m2 = 4.591
m3 = 2.374e-4
m4 = 5.304e-2
m5 = 1.340
m6 = 1.630e-2
m7 = 1.675e-7
m8 = 1.025e-2
m9 = 7.139e-13

def speedofsound(temp,salt,depth):
    """
    Calculate the speed of sound using the Mackenzie equation
    """
    return m1                             + \
        np.multiply(m2,temp)              - \
        np.multiply(m3,tsquared)          + \
        np.multiply(m4,tcubed)            + \
        np.multiply(m5,saltminus35)       + \
        np.multiply(m6,depth)             + \
        np.multiply(m7,depthsquared)      - \
        np.multiply(np.multiply(m8,temp),saltminus35) - \
        np.multiply(np.multiply(m9,temp),depthcubed)

def sos_unc2(inputFile):
    brack1 = T_uncsquared*(m2 + 2*m3*temp + 3*m4*tsquared + m8*saltminus35 + m9*depth3d)**2
    brack2 = S_uncsquared*(m5 + m8*temp)**2
    brack3 = D_uncsquared*(m6 + 2*m7*depth3d + 3*m9*temp*depthsquared)**2
    sos_unc = np.sqrt(brack1+brack2+brack3)
    date = str(inputFile[38:44])
    #date = str(inputFile[24:30])
    output_name = 'unc/sos_'+date+'_unc.nc'
    save_netcdf(output_name, data = sos_unc, depth=depth, lat=lat, lon=lon, standard_name='SOS_unc', units='m/s')
    print('completed', date)
    return np.sqrt(brack1+brack2+brack3), date
