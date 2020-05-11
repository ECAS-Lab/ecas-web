"""
Training with ECAS: a complete workflow for the computation and visualization of a climate indicator
====================================================================================================

This notebook guides you through the implementation and execution of a sample climate indicator exploiting the features provided by the *ECAS* environment and, in particular, those provided by the **Ophidia Framework**. The *ENES Climate Analytics Service* (ECAS) is one of the *EOSC-Hub Thematic Services*. It builds on top of the Ophidia big data analytics framework with additional components and services from the INDIGO-DataCloud software stack, EUDAT and EGI e-infrastructures.

The goal of this training is to give an overview of the features available in ECAS while implementing a real indicator from the *extreme climate indices* set. This list comprises 27 indices based on daily temperatures or daily precipitation amount, defined with the purpose to analyze extreme events. The indicator that you're going to implement during this training is the *Daily temperature range (DTR)*: i.e. the monthly mean difference between the maximum and minimum daily temperatures. The full list of indices is provided [http://etccdi.pacificclimate.org/list_27_indices.shtml](http://etccdi.pacificclimate.org/list_27_indices.shtml).

The training session will be completely carried out in this Jupyter Notebook using python code and the set of modules and libraries available in the ECASlab. Among these, one of the main modules is PyOphidia, the Ophidia python bindings, which integrates the features to interact with the Ophidia Framework, B2DROP and python environment. Please run the code blocks in the order specified to avoid any issue.

This session focuses on the PyOphidia module but if you are interested in learning additional features related to the Ophidia Framework, you can check the official documentation on the [Ophidia website](http://ophidia.cmcc.it/documentation). 

Before starting the actual implementation of the indicator, let's play a little with the basic features of PyOphidia.
"""
#!/usr/bin/env python
# coding: utf-8

# <img src="imgs/ecas_logo.png" alt="ECAS Logo" width="500">
# 
# 
# # Training with ECAS: a complete workflow for the computation and visualization of a climate indicator
# 
# This notebook guides you through the implementation and execution of a sample climate indicator exploiting the features provided by the *ECAS* environment and, in particular, those provided by the **Ophidia Framework**. The *ENES Climate Analytics Service* (ECAS) is one of the *EOSC-Hub Thematic Services*. It builds on top of the Ophidia big data analytics framework with additional components and services from the INDIGO-DataCloud software stack, EUDAT and EGI e-infrastructures.
# 
# The goal of this training is to give an overview of the features available in ECAS while implementing a real indicator from the *extreme climate indices* set. This list comprises 27 indices based on daily temperatures or daily precipitation amount, defined with the purpose to analyze extreme events. The indicator that you're going to implement during this training is the *Daily temperature range (DTR)*: i.e. the monthly mean difference between the maximum and minimum daily temperatures. The full list of indices is provided [http://etccdi.pacificclimate.org/list_27_indices.shtml](http://etccdi.pacificclimate.org/list_27_indices.shtml).
# 
# The training session will be completely carried out in this Jupyter Notebook using python code and the set of modules and libraries available in the ECASlab. Among these, one of the main modules is PyOphidia, the Ophidia python bindings, which integrates the features to interact with the Ophidia Framework, B2DROP and python environment. Please run the code blocks in the order specified to avoid any issue.
# 
# This session focuses on the PyOphidia module but if you are interested in learning additional features related to the Ophidia Framework, you can check the official documentation on the [Ophidia website](http://ophidia.cmcc.it/documentation). 
# 
# Before starting the actual implementation of the indicator, let's play a little with the basic features of PyOphidia.

# ## 1. Getting started with PyOphidia
# 
# PyOphidia is a Python package used to interact with the Ophidia Framework and it provides a convenient way to submit requests to an Ophidia server or to develop your own application using Python. It runs on Python 2 or 3 and provides 2 main modules:
# 
# * client.py: low level class to submit any type of requests (simple tasks and workflows);
# * cube.py: high level cube-oriented class to interact directly with cubes.
# 
# This tutorial will mainly exploit the cube class feature.
# 
# Before running any other operation, a new session with the Ophidia Server must be established. Run the following code cell to set a new connection by pressing the **play** button on the top bar or **[shift + enter] keys**. 
# 

# In[ ]:


from PyOphidia import cube
cube.Cube.setclient(read_env=True)


# If successful, the output will show something like:
#     
# ```python
# Current session is https://ophidialab.cmcc.it/ophidia/sessions/456546436462436547544775644646/experiment
# Current cwd is /
# The last produced cube is https://ophidialab.cmcc.it/ophidia/1/1
# ```

# Once the connection has been established, it's possible to run the actual data management and analytics operators. 
# 
# The first operator to test is *list*, which provides a graphical (ASCII-based) view of the data available in the user's space. It is worth mentioning that Ophidia manages a virtual file system associated with each single user that provides a hierarchical organization of concepts, supporting: 
# 
# * *datacubes*, the actual objects containing the dataset variables, dimensions and related metadata;
# * *containers*, grouping together a set of related datacubes, i.e. those concerning the same set of dimensions; 
# * *virtual folders*, to store one or more containers according to the user's needs. 
# 
# If this is the first experiment you're running, your space should be empty, otherwise you'll see some Ophidia containers/datacubes created in the previous sessions. Try it yourself by running the following line.

# In[ ]:


cube.Cube.list(level=2)


# Now it's time to load the first dataset into your space by exploiting the *importnc* operator. Run the following command to load a CMIP5 NetCDF (*.nc*) dataset produced by [*CMCC Foundation*](https://www.cmcc.it) with the *CESM model* creating a new datacube. It should take a few seconds.
# 
# As you can see, the method uses a lot of different arguments to load the data. For this tutorial, you can ignore most of them and just focus on the two most important ones:
# 
# * *src_path*, the path of the file to be imported
# * *measure*, the variable to be imported (*tasmax*, the maximum daily temperature)
# 
# If you want to learn more about all the parameters available in the *importnc* operator, you can check the [documentation page](http://ophidia.cmcc.it/documentation/users/operators/OPH_IMPORTNC.html).

# In[ ]:


# get_ipython().run_cell_magic('time', '', "tasmax = cube.Cube(\n    src_path='/public/data/ecas_training/tasmax_day_CMCC-CESM_rcp85_r1i1p1_20960101-21001231.nc',\n    measure='tasmax',\n    imp_dim='time',\n    import_metadata='yes',\n    imp_concept_level='d',\n    ncores=1,\n    description='Max Temperatures',\n    hierarchy='oph_base|oph_base|oph_time',\n    vocabulary='CF',\n    ioserver='ophidiaio_memory'\n    )")


# You can now import the second dataset related to the *tasmin* variable, i.e. the minimum daily temperature. 
# 
# Note the different value used for the **ncores** parameter. The Ophidia Framework provides an environment for the execution of parallel data analytics exploiting the underlying cluster features. This time the operator will run the import with 4 parallel processes and the execution time should take less. Compare the execution time shown in the output of the 2 cells. 

# In[ ]:


# get_ipython().run_cell_magic('time', '', "tasmin = cube.Cube(\n    src_path='/public/data/ecas_training/tasmin_day_CMCC-CESM_rcp85_r1i1p1_20960101-21001231.nc',\n    measure='tasmin',\n    imp_dim='time',\n    import_metadata='yes',\n    imp_concept_level='d',\n    ncores=4,\n    description='Min Temperatures',\n    hierarchy='oph_base|oph_base|oph_time',\n    vocabulary='CF',\n    ioserver='ophidiaio_memory'\n    )")


# At this stage you should have at least 2 containers and 2 datacubes inside your space. You can run again the *list* operator to verify this yourself. Datacubes are identified by a string that looks like:  `https://ophidialab.cmcc.it/ophidia/1/1`

# In[ ]:


cube.Cube.list(level=2)


# If you observe carefully the last two executed python lines, you'll notice that the methods are called in a slightly different way. 
# 
# In fact, all operators that create a new datacube in the user's space, like *importnc*, are categorized as *data operators* and produce as output a python Object enclosing the information regarding that datacube. In this way, it is possible to apply operators directly on the cube Object without the necessity to refer to the datacube identifier.
# 
# On the other hand, the operators that don't create a datacube, such as *list*, are categorized as *metadata operators* and are actually Class Methods that simply produce a visual output without any callable Object.
# 
# To see the list of all the Methods and Class Methods implemented in PyOphidia, you can run the following command. As you may note from the output length, there are plenty of Methods and Class Methods available. An examination of the full list of these methods is out of the scope of this training session. 

# In[ ]:


help(cube)


# You're now ready to run some analytical operations on the newly imported datacubes. The next section will guide you through some basic data analysis operations required for the DTR indicator.

# ## 2. Running data analytics operations
# 
# You can run different type of operations on the datacubes available in your space. Ophidia provides around 50 data and metadata operators supporting operations including: data aggregations, complex mathematical operations, predicate evaluation, subsetting, datacube intercomparison, metadata management, as well as import and export of datacubes ([check this page for the full list](http://ophidia.cmcc.it/documentation/users/operators/index.html)).
# 
# In this section, you'll see some of the most common operators and how these can be applied to compute the DTR indicator.
# 
# As stated in the previous section, operators applied to datacubes require a python Object referencing that cube. In the last code block we created the **tasmin** cube Object, so now we can apply other operations to this datacube.
# 
# The following cell code will perform a simple data reduction operation (i.e. the average over the whole time range) on the **tasmin** cube Object and produce another cube Object called **testCube1**. The parameters in the function specify the type of operations to be performed. The following commands show the information related to this newly created datacube and a portion of its content (note that these don't create any new datacube). Have a look in particular at the section regarding *Dimension Information* to check the data dimensionality.

# In[ ]:


testCube1 = tasmin.reduce2(
    dim='time',
    concept_level='A',
    operation='avg',
    description="Overall average tasmin",
    ncores=2    
)

testCube1.info()
testCube1.explore(limit_filter=1)


# You can also compute other types of statistical values over different time ranges. The *reduce2* operator [documentation page](http://ophidia.cmcc.it/documentation/users/operators/OPH_REDUCE2.html) provides the full description of the alternatives implemented by the operator.
# 
# Try to rerun the code above by replacing the following arguments to get the maximum temperature on a yearly basis and check the difference in the *Dimension Information* section.
# * concept_level='y'
# * operation='max'
# 
# Operations can also be applied in cascade in a single line of code, like in the following line, which computes the average over all datacube dimensions. The resulting **testCube2** Object will reference the final datacube created by the sequence of operations. 

# In[ ]:


testCube2 = tasmin.reduce(operation='avg', ncores=2).merge().aggregate(operation='avg', description="Mean tasmin")


# Most of the Ophidia data operators working on datacubes are applied on a cube Object and produce another cube Object, however some operators require more than one input datacube, like the *intercomparison*. In this case the additional datacubes must be specified in specific arguments. 
# 
# Now that you've seen some of the basic features available in Ophidia, let's get back to the implementation of the DTR indicator exploiting the concepts that you've just learned. 
# 
# The following code will, first of all, compute the daily temperature range with the *intecomparsion* operator, i.e. the difference among the **tasmax** datacube and the **tasmin** datacube, creating a new cube Object called **dailyDTR**. The second datacube is specified in the *cube2* argument. The following line computes the monthly mean values from the daily temperature ranges with the *reduce2* operator, creating a new Object **monthlyDTR**.

# In[ ]:


dailyDTR = tasmax.intercube(
    cube2=tasmin.pid,
    operation='sub',
    description="Daily DTR",
    measure='dtr',
    ncores=2
    )

monthlyDTR = dailyDTR.reduce2(
    dim='time',
    concept_level='M',
    operation='avg',
    description="Monthly DTR",
    ncores=2    
    )

monthlyDTR.explore(limit_filter=5)


# ## 3. Extracting the results of the computation
# 
# Now that you've applied some operations to the original imported data, it's time to check the results of the processing. Ophidia allows exporting the datacube as a NetCDF file and, thanks to the seamless integration with the python environment, it is possible to export it in python-friendly structures and plot it using well-known python modules, such as matplotlib, basemap and cartopy.
# 
# The datacube created in the previous step (**monthlyDTR**) contains the data for several months in the time range [2096-2100]. We would like to plot the data on a map so, for the sake of simplicity, let's extract a single time step (in the example *January 2096*) with the following code.

# In[ ]:


firstMonthDTR = monthlyDTR.subset2(
    subset_dims='time',
    subset_filter='2096-01',
    description="Subset Monthly DTR",
    ncores = 4
)

data = firstMonthDTR.export_array()


# The final row of the cell above allows exporting the data related to the **firstMonthDTR** datacube in a python-friendly structure, which can then be used as input for the plotting libraries.
# 
# You can explore the info contained in this structure with the following command. As you can see, the structure contains an array of values for each dimension (i.e. *lat*, *lon*, *time*) and variable (*dtr*) belonging to the datacube.

# In[ ]:


from IPython.lib.pretty import pprint
pprint(data)


# Finally, let's create a simple map with the DTR data extracted so far. The following code will create a map exploiting matplotlib and basemap libraries showing the DTR for the various points on the globe. 
# 
# You're free to change the properties to update the graphical layout. Check the basemap documentation for additional examples ([http://basemaptutorial.readthedocs.io/en/latest/basic_functions.html](http://basemaptutorial.readthedocs.io/en/latest/basic_functions.html)).
# 
# Note how the values from the dimensions *lat* and *lon* are used to define the map grid.

# In[ ]:


get_ipython().run_line_magic('matplotlib', 'inline')

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap, cm
import numpy as np

lat = data['dimension'][0]['values'][:]
lon = data['dimension'][1]['values'][:]
var = data['measure'][0]['values'][:]
var = np.reshape(var, (len(lat), len(lon)))

fig = plt.figure(figsize=(15, 15), dpi=100)
ax  = fig.add_axes([0.1,0.1,0.8,0.8])

map = Basemap(projection='cyl',llcrnrlat= -90,urcrnrlat= 90, llcrnrlon=0,urcrnrlon=360, resolution='c')

map.drawcoastlines()
map.drawparallels(np.arange( -90, 90,30),labels=[1,0,0,0])
map.drawmeridians(np.arange(-180,180,30),labels=[0,0,0,1])

x, y = map(*np.meshgrid(lon,lat))

clevs = np.arange(0,20,1)

cnplot = map.contourf(x,y,var,clevs,cmap=plt.cm.jet)
cbar = map.colorbar(cnplot,location='right')

plt.title('DTR')
plt.show()


# ## 4. Exercise: implement a second indicator
# 
# Now that you'we learned a bit of Ophidia, it's your turn to implement another climate indicator from the same set. In this section you're going to implement the *Number of summer days (SU)* indicator, i.e. the annual count of days when the daily maximum temperature is bigger than the reference temperature 25°C (it is very similar to *tropical nights index*). Please refer again to [http://etccdi.pacificclimate.org/list_27_indices.shtml](http://etccdi.pacificclimate.org/list_27_indices.shtml) for further information.
# 
# Some hints to implement this indicator:
# 
# 1. you can rely the code from the previous examples;
# 2. you can reuse the *tasmax* datacube created for the DTR indicator;
# 2. in order to get the days with temperature above 25°C (i.e., 298.15°K) you can use the predicate evaluation operation. This is the trickiest part of the indicator computation, an example of such operation is:
# ```python
# mycube.apply(query="oph_predicate('OPH_FLOAT','OPH_INT',measure,'x-298.15','>0','1','0')")
# ```
# The query parameter specifies the operation to be applied on each value within the datacube. In particular, it applies a predicate evaluation which converts all numbers bigger than 25 °C (the dataset contains Kelvin values, i.e. 298.15) to 1s and all the others to 0s. Additional information on this function is available on the [oph_predicate documentation](http://ophidia.cmcc.it/documentation/users/primitives/OPH_PREDICATE.html). 
# 
# 3. count the 1 days by using the *reduce2* operator applied on yearly basis with *sum* operation;
# 4. to plot the map you can run a *subset* operation followed by the same plotting code used previously.
# 
# Let's start!

# In[ ]:


### First, apply the predicate function on the tasmin cube already importd
summerDays = tasmax.apply(...)

#Second, run a yearly reduce2 on the previous cube
count = summerDays.reduce2(
    operation=...,
    dim=...,
    concept_level=...,
)

#Third, extract the first year for plotting purposes
firstYear = count.subset(
    subset_filter=..., 
    subset_dims=...
)

data = firstYear.export_array()

#Fourth, plot the data (you can reuse the code from the previous map example)


# You can find the an example for the implementation of this exercise in the *notebooks* folder on ECASLab in the [**Summer Days notebook**](Summer_Days.ipynb) notebook.

# ## 5. Final remarks
# 
# Congrats! You've completed this training regarding some basics operations that can be performed within the ECASlab and you should now be able to:
# 
# * use the PyOphidia module to implement a real-world climate indicator;
# * plot the experiment output on a map exploiting the modules integrated in the environment.
# 
# Of course, this training is not exhaustive; Ophidia provides a very wide range of operators to implement almost every type of indicator or use case. Have a look at the documentation or other example notebooks to explore the full potential of the environment.
# 
# If you want to clear your user space before running other notebooks, run the following commands:

# In[ ]:


cube.Cube.deletecontainer(container='tasmin_day_CMCC-CESM_rcp85_r1i1p1_20960101-21001231.nc',force='yes')
cube.Cube.deletecontainer(container='tasmax_day_CMCC-CESM_rcp85_r1i1p1_20960101-21001231.nc',force='yes')


# ## References
# 
# 1. [Ophidia website](https://ophidia.cmcc.it/)
# 2. [EOSC-Hub project website](https://www.eosc-hub.eu)
# 3. [PyOphidia library](https://github.com/OphidiaBigData/PyOphidia)
