#Step 5 - Variogram map

#Install packages
install.packages('gstat')
install.packages('sp')
#Import libraries
library(gstat)
library(sp)

#Functions

variogram_map <- function(df) {
  
  #variogram_map make the variogram map of points giving the dataframe with 
  #location and value of each point.
  
  #:param df: Dataframe of location and points of each point.
  #:return vmap_plot: Variogram plot of the points. 
  
  if(deparse(substitute(df)) == 'df_rainfall') {
    value <- Annual.Rainfall..mm. ~ 1
  } else {
    value <- Hurst.Exponent ~ 1
  }
  variomap <- variogram(gstat(id = 'Variogram map',formula= value , data=df), 
                        map = TRUE , cutoff = 500000, width = 35000)
  return(variomap)
}

#Set working director
path <- 'C:/Users/USER/Documents/Kriging Project/'
setwd(path)

#Stations info file
stations_info <- read.csv(file = paste(path, 'Aditional File 1.csv', sep = ''), 
                        encoding = 'UTF-8')

#Rainfall dataframe
df_rainfall <- stations_info[1:6]
#Hurst dataframe
df_hurst <-  stations_info[c(1:5,7)]

# Coordinates in dataframes
coordinates(df_rainfall) <- ~ Latitude.UTM..m. + Longitude.UTM..m.
coordinates(df_hurst) <- ~ Latitude.UTM..m. + Longitude.UTM..m.

#Variogram map for rainfall 
variomap_rainfall <- variogram_map(df_rainfall)
plot(variomap_rainfall , threshold = 0.1)

#variogram map for hurst
variomap_hurst <- variogram_map(df_hurst)
plot(variomap_hurst , threshold = 0.1)