"""
Demo: Export datacubes and files to EUDAT B2DROP
================================================

In this demo we will run some data analytics, create some plots and export the dataset and plot produced during these stages on our B2DROP folder.

Pre-requisite 1: a B2DROP account is required. You can login to B2DROP through B2ACCESS.

Pre-requisite 2: a NetCDF file in your B2DROP space (base folder).

Pre-requisite 3: a specific Application Password to be used for the file sharing through Ophidia, in order to avoid the sharing of the actual password with external applications.
"""
#!/usr/bin/env python
# coding: utf-8

# # Demo: Export datacubes and files to EUDAT B2DROP

# In this demo we will run some data analytics, create some plots and export the dataset and plot produced during these stages on our B2DROP folder.
# 
# **Pre-requisite 1:** a B2DROP account is required. You can login to B2DROP through B2ACCESS.
# 
# **Pre-requisite 2:** a NetCDF file in your B2DROP space (base folder).
# 
# **Pre-requisite 3:** a specific *Application Password* to be used for the file sharing through Ophidia, in order to avoid the sharing of the actual password with external applications.
# 
# <img src="imgs/b2drop_setup.png" alt="B2DROP Setup" width="1000">
# 
# 
# After clicking on the *Create new app password* button a new password will be create. **The credentials will be shown just once so we need to store them before clicking on the *complete* button.**

# In[ ]:





# Create a new **.netrc** file in the home directory with the credentials just generated (like in the example). This file will be used by Ophidia to authenticate to the B2DROP account and upload the files.

# In[1]:


# get_ipython().run_cell_magic('bash', '', "> $HOME/.netrc\ncat <<'EOF' >> $HOME/.netrc\nmachine <B2DROP service>\nlogin  <username>\npassword <password>\nEOF\nchmod 0600 $HOME/.netrc")


# We can now download the NetCDF file from our B2DROP space, but before let's change the current folder used by Ophidia

# In[2]:


from PyOphidia import cube, client
cube.Cube.setclient(read_env=True)

cube.Cube.fs(command='cd',
             dpath='/home/'+cube.Cube.client.username+'/', 
             display=True)


# PyOphidia allows to download files from our B2DROP space by running the following *class method* (this is internally using the B2DROP APIs)

# In[3]:


cube.Cube.b2drop(src_path='tos.nc',action='get',dst_path='tos-b2drop.nc')


# A new file named tos.nc will be available under the base folder /

# In[ ]:


get_ipython().run_cell_magic('bash', '', 'ls -l $HOME/*.nc')


# Let's now import the dataset downloaded from B2DROP and run some basic operations.

# In[ ]:


from PyOphidia import cube, client
cube.Cube.setclient(read_env=True)

mycube = cube.Cube.importnc(src_path='tos-b2drop.nc', measure='tasmax', imp_dim='time', import_metadata='yes', 
                            imp_concept_level='d', ncores=2, hierarchy='oph_base|oph_base|oph_time', 
                            ioserver='ophidiaio_memory')

mycube2 = mycube.reduce(operation='max',ncores=2)

mycube2.info()


# Recall that the current folder is:

# In[ ]:


cube.Cube.fs(command='ls', display=True)


# To export into a nc file called tos.nc

# In[ ]:


mycube2.exportnc2(output_path='./',output_name='tos-ophidia')


# A new file name *tos-ophidia.nc* will be available under the base folder */*

# In[ ]:


get_ipython().run_cell_magic('bash', '', 'ls -l $HOME/*.nc')


# We can reuse the PyOphidia *class method* also to upload data to the B2DROP space

# In[ ]:


cube.Cube.b2drop(src_path='tos-ophidia.nc',action='put')


# Let's try to create a map with the datacube previously computed and store the file as *map.png*

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm, addcyclic, shiftgrid
import numpy as np

data = mycube2.export_array()
lat = data['dimension'][0]['values'][:]
lon = data['dimension'][1]['values'][:]
var = data['measure'][0]['values'][:]

fig = plt.figure(figsize=(15, 15), dpi=100)
ax  = fig.add_axes([0.1,0.1,0.8,0.8])

map = Basemap(projection='cyl',llcrnrlat=-90,urcrnrlat=90, llcrnrlon=-180,urcrnrlon=180, lon_0=0, resolution='c')

map.drawcoastlines()
map.drawparallels(np.arange( -90, 90,30),labels=[1,0,0,0])
map.drawmeridians(np.arange(-180,180,30),labels=[0,0,0,1])

var = np.reshape(var, (len(lat), len(lon)))
var_cyclic, lon_cyclic = addcyclic(var, lon)
var_cyclic, lon_cyclic  = shiftgrid(180., var_cyclic, lon_cyclic, start=False)
x, y = map(*np.meshgrid(lon_cyclic,lat))

levStep = (np.max(var)-np.min(var))/30
clevs = np.arange(np.min(var),np.max(var)+levStep,levStep)

cnplot = map.contourf(x,y,var_cyclic,clevs,cmap=plt.cm.jet)
cbar = map.colorbar(cnplot,location='right')

plt.title('Maximum Temperature (deg K)')
plt.savefig('map.png',  bbox_inches='tight')
plt.show()


# Using the PyOphidia method we can upload any type of file on B2DROP (we don't need to specify the *action* argument, since upload is the default action)

# In[ ]:


cube.Cube.b2drop(src_path='./map.png')


# In a more integrated fashion, we can directly export a datacube into a NetCDF remotely stored on the B2DROP space.

# In[ ]:


mycube2.to_b2drop()


# To clear your workspace before running other notebooks

# In[ ]:


cube.Cube.deletecontainer(container='tos-b2drop.nc',force='yes')

