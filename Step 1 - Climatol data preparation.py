# 1 STEP - Climatol data preparation

#Import libraries
import pandas as pd
import numpy as np
import os
import glob
import itertools as it
import matplotlib.pyplot as plt

#Import the data
#Path of working directory
path = 'C:/Users/USER/Documents/Kriging Project'
os.chdir(path)
path_stations = path+'/Stations/'
files = glob.glob(path_stations + '*.csv')
filenames = [file.replace('.csv', '') for file in next(os.walk(path_stations))[2]]

#Number of data in each year
total_data = pd.Series()
for file in files:
  df = pd.read_csv(file)
  df = df.set_index('Year')
  station_data = df.count(axis=1)
  total_data= {k: dict(total_data).get(k, 0) + dict(station_data).get(k, 0) 
               for k in set(dict(total_data)) | set(dict(station_data))}

df_total_data = pd.DataFrame(total_data.items(), columns=['Year','Data'])
df_total_data = df_total_data.set_index('Year')
#Total data per year
plt.figure()
plt.plot(df_total_data.index,df_total_data.Data)
#Top 30 years with more data
top_data = df_total_data.sort_values('Data', 
                                     ascending=False)[:30].sort_values('Year')
print('Top 30 of stations with more data:')
print(top_data)
#Selecting the period of 1998 to 2018
plt.figure()
plt.plot(df_total_data.loc['1998':'2018'])
plt.xticks(np.arange(1998, 2019, 2))

#Percentage of original data by station between 1998 and 2018
percentage = []
for file in files:
  df = pd.read_csv(file,index_col='Year')
  percentage.append(df.loc[1998:2018].count().sum()/(12*21)*100)
station_perc = pd.DataFrame(list(zip(files,filenames, percentage)),
                            columns =['File','Station', 'Percentage']) 
#Selecting only the stations with more of 80% of original data
station_filt = station_perc[station_perc['Percentage']>=80].sort_values('Station')
station_filt = station_filt.reset_index(drop=True)
print('Mean of the porcentage of original data:')
print(station_filt.mean(numeric_only=True))

#Getting the monthly rainfall data of the selected stations
values = []
idx = np.arange(1998,2018 + 1, 1)
for file in station_filt['File']:
  df = pd.read_csv(file,index_col='Year')
  values.append(list(it.chain.from_iterable(df.loc[1998:2018].reindex(idx)
                                            .values.tolist())))
#Climatol dat file
climatol_dat = pd.DataFrame(values)
#Change the path to save the file
os.makedirs('Climatol')
climatol_dat.to_csv(path + '/Climatol/Rmon_1998-2018.dat', sep='\t', 
                na_rep='NA',index=False,header=False)

#Reading the information file of each station
station_info = pd.read_csv(path + '/Aditional File 1.csv')
#Getting the info of the selected stations
station_info_filt = station_info[station_info['Station Name']
                                 .isin(station_filt['Station'])]

clim_dict = {'Longitude' : station_info_filt['Longitude UTM (m)'],
            'Latitude' : station_info_filt['Latitude UTM (m)'],
            'Elevation' : station_info_filt['Elevation (masl)'],
            'Code' : '\'' + station_info_filt['Code'].astype(str) + '\'',
            'Station' : '\'' + station_info_filt['Station Name'].astype(str) + '\''}
climatol_est = pd.DataFrame(clim_dict)

#Climatol est file
climatol_est.to_csv(path + '/Climatol/Rmon_1998-2018.est', sep='\t', 
                na_rep='NA',index=False,header=False)
