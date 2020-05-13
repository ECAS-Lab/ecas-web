"""
Demo: ECAS/Ophidia simple commands examples
===========================================

First of all import PyOphidia modules and connect to server (connection details are inferred from the ECAS environment)
"""
#!/usr/bin/env python
# coding: utf-8

# # Demo:  ECAS/Ophidia simple commands examples

# First of all import PyOphidia modules and connect to server (connection details are inferred from the ECAS environment)

# In[ ]:


from PyOphidia import cube, client
cube.Cube.setclient(read_env=True)


# Create a datacube from the NetCDF file:
# - The file is **/public/data/ecas_training/tos_O1_2001-2002.nc**
# - The variable to be imported is **tos**
# - Data should be arranged in order to operate on time series (**time** dimension) 
# 
# **Note: We are not directly reading the file from the Notebook**

# In[ ]:


mycube = cube.Cube.importnc(
                src_path='/public/data/ecas_training/tos_O1_2001-2002.nc',
                measure='tos',
                imp_dim='time',
                ioserver='ophidiaio_memory',
                ncores=2,
                description="Imported cube"
        )


# Check the datacubes available in the virtual file system

# In[ ]:


cube.Cube.list(level=2)


# To get the list of arguments and default values we can use the python *help()* command can be used

# In[ ]:


help(cube.Cube.list)


# Inspect the cube and its dimensions structure

# In[ ]:


mycube.info()


# Subset the datacube over space (lat and lon) and time
# 
# **Note: each instance method produces a new datacube object**

# In[ ]:


mycube2 = mycube.subset(
                subset_dims="lat|lon|time",
                subset_filter="-80:30|30:120|151:240",
                subset_type="coord",
                ncores=2,
                description="Subsetted cube"
        )


# Inspect the new cube; dimensions have been changed

# In[ ]:


mycube2.info()


# But what does the datacube actually contain at this point? We can use the explore method to check the content. 

# In[ ]:


mycube2.explore(limit_filter=1)


# We can then compute the maximum value over the time series for each point in the spatial domain

# In[ ]:


mycube3 = mycube2.reduce(
                    operation='max',
                    ncores=2,
                    description="Reduced cube"
                )


# In the new cube the time dimension is be "collapesed"

# In[ ]:


mycube3.info()


# We can now reorganize the data structure by making the longitude dimension an array-oriented dimension

# In[ ]:


mycube4 = mycube3.rollup(
                    ncores=2,
                    description="Rollup cube"
                )


# The new cube will now have *lon* has an array-dimension

# In[ ]:


mycube4.info()


# Each operation executed creates a new datacube on the framework (datacubes are not overwritten)

# In[ ]:


cube.Cube.list(level=2)


# Let's export the data into a Python-friendly structure. 
# 
# **Note: this is the first time we move data from the server-side to the Notebook**

# The structure looks something like this
# 
# <img src="imgs/export_array.png" alt="Export Array" width="800">
# 
# 

# In[ ]:


data = mycube4.export_array()

from IPython.lib.pretty import pprint
pprint(data)


# The data exported in the Python structure can be used to create a map (note the definition of a Python function)

# In[ ]:


# get_ipython().run_line_magic('matplotlib', 'inline')

def plotData(data):
    import matplotlib.pyplot as plt
    from mpl_toolkits.basemap import Basemap, cm
    import numpy as np

    lat = data['dimension'][0]['values'][:]
    lon = data['dimension'][1]['values'][:]
    var = data['measure'][0]['values'][:]

    fig = plt.figure(figsize=(15, 15), dpi=100)
    ax  = fig.add_axes([0.1,0.1,0.8,0.8])

    map = Basemap(projection='cyl',llcrnrlat= -90,urcrnrlat= 90, llcrnrlon=0,urcrnrlon=360, resolution='c')

    map.drawcoastlines()
    map.drawparallels(np.arange( -90, 90,30),labels=[1,0,0,0])
    map.drawmeridians(np.arange(-180,180,30),labels=[0,0,0,1])

    x, y = map(*np.meshgrid(lon,lat))

    cnplot = map.contourf(x,y,var,np.arange(270,305,0.5),cmap=plt.cm.jet)
    cbar = map.colorbar(cnplot,location='right',format='%.2f')

    plt.title('Sea Surface Temperature (deg K)')
    plt.show()
    
plotData(data)


# #### What If we want to consider the whole spatial domain and specify a subset only on the time range? 
# 
# We can perform the new set of operations on *mycube* object, without the need to re-import the dataset from the file. Note that we are providing the time range in human-readable form

# In[ ]:


newMycube2 = mycube.subset(
                subset_dims="time",
                subset_filter="2001-01-01_2001-12-31",
                subset_type="coord",
                time_filter="yes",
                ncores=2,
                description="New subsetted cube"
        )

newMycube2.info()


# We can the rerun the same operations on the new cube ...

# In[ ]:


newMycube3 = newMycube2.reduce(
                    operation='max',
                    ncores=2,
                    description="New reduced cube"
                )

newMycube4 = newMycube3.rollup(
                    ncores=2,
                    description="New rollup cube"
                )


# ... and plot the new datacube values on a map using the function *plotData*

# In[ ]:


data = newMycube4.export_array()
plotData(data)


# #### What if we want to get the *minimum* instead of the maximum value?
# 
# Again we can perform the new set of operations on *newMycube2* object, without the need to re-import or subset the dataset again

# In[ ]:


newNewMycube3 = newMycube2.reduce(
                    operation='min',
                    ncores=2,
                    description="New reduced cube2"
                )

newNewMycube4 = newNewMycube3.rollup(
                    ncores=2,
                    description="New rollup cube2"
                )


# ... and plot the new datacube values on a map using the function *plotData*

# In[ ]:


data = newNewMycube4.export_array()
plotData(data)


# Our workspace now contains several datacubes from the experiments just run. Once done, we can clear the space before moving to other notebooks. 
# 
# **Note: the *client.submit* is exploiting the underlying *PyOphidia client class* to submit commands in terminal-like syntax.**

# In[ ]:


cube.Cube.deletecontainer(container='tos_O1_2001-2002.nc',force='yes')


# The virtual file system should now be "clean"

# In[ ]:


cube.Cube.list(level=2)

