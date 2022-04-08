#Step 4 - Exploratory Data Analysis

#Import libraries
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from scipy.stats import skew
from scipy.spatial import Voronoi
from esda.moran import Moran
from esda.geary import Geary
from libpysal.weights.contiguity import Queen
import geopandas
from libpysal.weights import Rook
from pysal.lib import weights
from shapely.geometry import MultiPoint , Polygon
import glob
import itertools as it
import os

#Functions

def Area(df):
    
    """
    Area make a grid of points inside a polygon with 1000 units of space.
    
    :param df: The dataframe of coordinates of the perimeter of the polygon.
    
    """ 
    
    x=df['Latitude UTM (m)']
    y=df['Longitude UTM (m)']
    limit=np.column_stack((x,y))
    
    #Making the grid
    p = Polygon(limit)
    xmin , ymin , xmax , ymax = p.bounds
    x = np.arange(np.floor(xmin) , np.ceil(xmax) + 1 , 1000)
    y = np.arange(np.floor(ymin) , np.ceil(ymax) + 1 , 1000)
    points = MultiPoint(np.transpose([np.tile(x , len(y)) ,
                                      np.repeat(y , len(x))]))
    points = list(points.intersection(p))
    
    #Points to a csv document
    coordinates = []
    for pp in points:
        coordinates.append([pp.x , pp.y])
    coordinates = np.array(coordinates)
    df_points = pd.DataFrame(coordinates , columns = ['Latitude UTM (m)' ,
                                                      'Longitude UTM (m)'])
    return df_points

def Map(df):
    
    """
    Map make a map of given points inside a polygon with a color bar of the 
    value of the points.
    
    :param df: The dataframe of coordiantes and values of the points.
    
    """
    
    #Chosen dataframe
    df_name =[x for x in globals() if globals()[x] is df][0]
    if df_name == 'df_rainfall':
        value = 'Annual Rainfall (mm)'
    else:
        value = 'Hurst Exponent'
        
    x = df['Latitude UTM (m)']
    y = df['Longitude UTM (m)']
    z = df[value]
    plt.figure()
    #Perimeter plot
    plt.plot(df_limit['Latitude UTM (m)'] , df_limit['Longitude UTM (m)'] ,
             c='red')
    plt.axis('scaled')
    #Point plot
    ax = sns.scatterplot(x , y , z , palette='mako')
    norm = plt.Normalize(z.min(), z.max())
    sm = plt.cm.ScalarMappable(cmap="mako", norm=norm)
    sm.set_array([])
    ax.get_legend().remove()
    ax.set(xlabel='Latitude UTM (m)' ,
       ylabel='Longitude UTM (m)')
    plt.title(str(value), fontdict={'fontsize':10})
    ax.figure.colorbar(sm)
    plt.show()
    return

def Stationarity(df,idx):
    
    """
    Stationarity plot the values of each point sorted and its mean.
    
    :param df: The dataframe of values of the points.
    :param idx: Indicate how the points are going to be sorted
    
    """
    #Chosen dataframe
    df_name =[x for x in globals() if globals()[x] is df][0]
    if df_name == 'df_rainfall':
        value = 'Annual Rainfall (mm)'
    else:
        value = 'Hurst Exponent'
    
    #Sort
    df_sort = df.sort_values(idx)
    x_sort = df_sort[idx].reset_index(drop=True)
    z_sort = df_sort[value].reset_index(drop=True)
    plt.figure()
    plt.plot(z_sort , color = 'skyblue')
    for i in range(len(z_sort)):
        plt.scatter(i , z_sort[i] , color='blue')
    plt.hlines(z_sort.mean() , xmin=0 , xmax=len(z_sort) ,
               color='green' , label='Mean')
    #Change of ticks and names
    positions = np.linspace(0 , len(z_sort)-1 , 5 , dtype=int)
    labels = x_sort[positions]
    plt.xticks(positions, labels)
    plt.legend()
    plt.xlabel(idx)
    plt.ylabel(value)
    plt.title(str(value)+' for puvliometric stations')
    plt.show()
    return 

def Symmetry(df,bins):
    
    """
    Symmetry calculate the skewness of a distribution of z values and log(z) 
    values and plot it .
    
    :param df: The dataframe of values of the points.
    :param bins: Number of bins in histogram plot.
    
    """
    
    #Chosen dataframe
    df_name =[x for x in globals() if globals()[x] is df][0]
    if df_name == 'df_rainfall':
        value = 'Annual Rainfall (mm)'
    else:
        value = 'Hurst Exponent'
    
    z = df[value]
    plt.figure()
    plt.subplots(1,2,figsize=(15,5))
    plt.subplot(1, 2, 1)
    ax = sns.histplot(z , bins=bins , kde=True)
    ax.set( xlabel=value , ylabel='Frecuency')
    #Skewness of z values 
    print('\n The symmetry coefficient for '+str(value)+' is:',skew(z))
    z = np.log(df[value])
    plt.subplot(1, 2, 2)
    ax = sns.histplot(z , bins=bins , kde=True)
    ax.set( xlabel='Logarithmic'+str(value) , ylabel='Frecuency')
    #Skewness of log(z) values
    print('The symmetry coefficient for logarithmic '+str(value)+' is:',skew(z))
    return

def Autocorrelation(df):
    
    """
    Autocorrelation calculate the Moran´s I and Geary's C coefficients of 
    autocorrelation.
    
    :param df: The dataframe of values of the points.
    
    """
    
    #Chosen dataframe
    df_name =[x for x in globals() if globals()[x] is df][0]
    if df_name == 'df_rainfall':
        value = 'Annual Rainfall (mm)'
    else:
        value = 'Hurst Exponent'
    
    #Voronoi diagram
    ids = np.array(np.column_stack((df['Latitude UTM (m)'] ,
                                       df['Longitude UTM (m)'])))
    vor = Voronoi(ids)
    polygons = {}
    for id , region_index in enumerate(vor.point_region):
        points = []
        for vertex_index in vor.regions[region_index]:
            if vertex_index != -1:  # the library uses this for infinity
                points.append(list(vor.vertices[vertex_index]))
        points.append(points[0])
        polygons[id]=points

    polys=[]
    for i in range(len(polygons)):
        polys.append(Polygon(polygons[i]))
    polys = geopandas.GeoSeries(polys)
    gdf = geopandas.GeoDataFrame({'geometry' : polys , 
          'id' : ['P-%s'%str(i).zfill(2) for i in range(len(polys))]})
    
    #Coeficcients calculation
    wr = weights.contiguity.Rook.from_dataframe(gdf)
    wr.neighbors
    w=pd.DataFrame(*wr.full()).astype(int)
    w=Queen.from_dataframe(gdf)
    mi=Moran(df[value], w)
    c = Geary(df[value],w)
    print('\n Autocorrelation for '+str(value))
    print(' Moran´s I: ',mi.I,'Geary´s c: ',c.C)
    return


#Import the data
#Path of working directory
path = 'C:/Users/USER/Documents/Kriging Project/'
os.chdir(path)
#Perimeter of the study area
df_limit = pd.read_csv(path + 'Boundary.csv')
#Stations info
df_stations = pd.read_csv(path + 'Aditional File 1.csv')

#Slicing stations info dataframe into rainfall dataframe and hurst dataframe
df_rainfall = df_stations.iloc[:,0:6]
df_hurst = df_stations.iloc[:,np.r_[0:5,6]]

#Area

#Getting the points inside the study area
df_area = Area(df_limit)
df_area.to_csv(path + 'Area.csv' , index = False)


#Map of stations in the study area

#Rainfall Data
Map(df_rainfall)
#Hurst Exponent
Map(df_hurst)

#Spacial Stationarity

#Rainfall Data. Stations sorted by differents parameters 
#Parameters: latitude,longitude and elevation
Stationarity(df_rainfall , 'Latitude UTM (m)')
Stationarity(df_rainfall , 'Longitude UTM (m)')
Stationarity(df_rainfall , 'Elevation (masl)')
#Mean and variance
std_rainfall = np.sqrt(pd.Series.var(df_rainfall['Annual Rainfall (mm)']))
mean_rainfall = np.mean(df_rainfall['Annual Rainfall (mm)'])
print('\n Annual Rainfall (mm)')
print('Mean: ' , mean_rainfall , ' , Standard deviation: ' , std_rainfall)

#Huest Exponent. Stations sorted by differents parameters 
#Parameters: latitude,longitude and elevation
Stationarity(df_hurst , 'Latitude UTM (m)')
Stationarity(df_hurst , 'Longitude UTM (m)')
Stationarity(df_hurst , 'Elevation (masl)')
#Mean and variance
std_hurst = np.sqrt(pd.Series.var(df_hurst['Hurst Exponent']))
mean_hurst = np.mean(df_hurst['Hurst Exponent'])
print('\n Hurst Exponent')
print('Mean: ' , mean_hurst , ' , Standard deviation: ' , std_hurst)

#Symmetry of density functions

#Rainfall data symmetry
Symmetry(df_rainfall , 20)
#Hurst exponent data symmetry
Symmetry(df_hurst , 20)

#Moran´s and Geary´s Autocorrelation

#Rainfall Data
Autocorrelation(df_rainfall)
#Hurst Data
Autocorrelation(df_hurst)