#Step 6 - Variogram parameters

#Import libraries
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import skgstat as skg
from skgstat import models

#Functions

def Variogram(df,azimuth,tolerance,maxlag,nlags):
    
    """
    Variogram calculate the initial parameteres of theorical variograms
    that fit with the experimental variogram of exponential, gaussian and
    spherical models.
    
    :param df: The dataframe of values of the points.
    :param azimuth: Angle of direction of the variogram calculation.
    :param tolerance: Tolerance angle permited in the azimuthal direction.
    :param maxlag: Maximum distance of variogram calculation.
    :param nlags: Number of lags in between until the maximun distance.
    :return df_parameters: Dataframe of the resultant parameters
    
    """
    
    #Chosen dataframe
    df_name =[x for x in globals() if globals()[x] is df][0]
    if df_name == 'df_rainfall':
        value = 'Annual Rainfall (mm)'
    else:
        value = 'Hurst Exponent'
        
    #variogram calculation
    coords = np.column_stack((df['Latitude UTM (m)'],df['Longitude UTM (m)']))
    values = df[value]
    
    svg_models = np.array(['Exponential' , 'Gaussian' , 'Spherical'])
    svg_parameters=[]
    for model in svg_models:
        V = skg.DirectionalVariogram(coords , values , azimuth = azimuth , 
                                     tolerance = tolerance , maxlag = maxlag ,
                                     n_lags = nlags)
        V.fit_method = 'lm'
        V.model = model
        plt.figure()
        V.plot(hist=False)
        plt.xlabel('Distance (m)')
        plt.ylabel('Variance')
        plt.title(str(model) +  ' Variogram')
        parameters = V.parameters
        parameters.append(V.rmse)
        svg_parameters.append(parameters)
    svg_parameters = np.array(svg_parameters)
    df_parameters = pd.DataFrame(svg_parameters)
    df_parameters.insert(0,4,svg_models)
    df_parameters.rename(columns={4 : 'Model' , 0 : 'Range' ,
                                  1 : 'Sill' , 2 : 'Nugget' , 3 : 'RMSE'}, 
                         inplace = True)
    return df_parameters

#Import the data
#Path of working directory
path = 'C:/Users/USER/Documents/Kriging Project/'
os.chdir(path)
#Stations info
df_stations = pd.read_csv(path + 'Aditional File 1.csv')

#Slicing stations info dataframe into rainfall dataframe and hurst dataframe
df_rainfall = df_stations.iloc[:,0:6]
df_hurst = df_stations.iloc[:,np.r_[0:5,6]]

#Variogram of rainfall data
df_rainfall_parameters = Variogram(df_rainfall, 130, 40, 150000, 20)
df_rainfall_parameters.to_csv(path + 'Rainfall Parameters.csv', index = False )
#Variogram of hurst data
df_hurst_parameters = Variogram(df_hurst, 130, 40, 100000, 15)
df_hurst_parameters.to_csv(path + 'Hurst Parameters.csv', index = False )