def create_master(path, variable):
    """
    This method is used to combine monthly cubes into one master cube. Dealing with one big cube is much faster than looping through a directory so is done in the name of computational efficiency
    """
    list_of_cubes = []
    count = 0
    for my_file in glob.glob(path+'\*.nc'):
        cube = iris.load_cube(my_file)
        new_coord = iris.coords.AuxCoord(count, standard_name='time')
        cube.add_aux_coord(new_coord)
        list_of_cubes.append(cube)
        count += 1
    cube_list = iris.cube.CubeList(list_of_cubes)
    master = cube_list.merge_cube()
    iris.save(master, 'master_'+str(variable)+'.nc')
    print('Completed master cube')
