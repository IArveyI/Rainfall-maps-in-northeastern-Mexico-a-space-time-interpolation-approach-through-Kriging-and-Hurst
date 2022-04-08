#Step 7 - Kriging maps

#Install packages
install.packages('gstat')
install.packages('sp')
install.packages('dplyr')
install.packages('ggplot2')
install.packages('scales')
install.packages('magrittr')
install.packages('zeallot')
install.packages('Cairo')
#Import libraries
library(gstat)
library(sp)
library(dplyr)
library(ggplot2)
library(scales) 
library(magrittr)
library(zeallot)
library(Cairo)

#Functions

kriging <- function(df, model, range, sill, nugget, area){
  
  #Kriging make the variogram with the best fit parameters, make the Kriging
  #and variance plots and cross-validation calculation.
  
  #:param df: Dataframe of location and points of each point.
  #:param model: Model of semivariogram to use.
  #:param range: Effective range parameter in semivariogram.
  #:param sill: Range paramater in semivariogram.
  #:param nugget: Nugget parameter in semivariogram.
  #:param num_lag: Number of lags in semivariogram calculation.
  #:param max_lag: Maximum lag in semivariogram calculation.
  #:param area: Dataframe of the points of the area to interpolate.
  #:return semivariogram_plot: Variogram plot of the points.
  #:return kriging_plot: Kriging plot of the points.
  #:return variance_plot: Variance plot of the points.
  #:return cross_validation: Cross validations of the Kriging interpolation.
  
  if(deparse(substitute(df)) == 'df_rainfall') {
    value <- Annual.Rainfall..mm. ~ 1
  } else {
    value <- Hurst.Exponent ~ 1
  }
  
  vgm <- vgm(psill = sill, model, range = range, nugget)
  
  lzn.kriged <- krige(value , df , area , model=vgm)
  
  kriging_plot <- lzn.kriged %>% as.data.frame %>%
    ggplot(aes(x=Latitude.UTM..m. , y=Longitude.UTM..m.)) + geom_tile(aes(fill=var1.pred)) + coord_equal() +
    scale_fill_gradient(low = "yellow" , high="red") +
    scale_x_continuous(labels=comma) + scale_y_continuous(labels=comma) +
    theme_bw()
  
  variance_plot <- lzn.kriged %>% as.data.frame %>%
    ggplot(aes(x=Latitude.UTM..m., y=Longitude.UTM..m.)) + geom_tile(aes(fill=var1.var)) + coord_equal() +
    scale_fill_gradient(low = "yellow", high="red") +
    scale_x_continuous(labels=comma) + scale_y_continuous(labels=comma) +
    theme_bw()
  
  cross_validation <- krige.cv(value, df, vgm, nfold=10)
  
  return(list(kriging_plot,variance_plot,cross_validation))
}

cross_validation <- function(cv, model){
  #cross_validation make a dataframe of errors giving a cross validation dataframe. 
  
  #:param cv: Cross validation dataframe.
  #:param model: Kriging model of the cross validation dataframe.
  #:return df: Dataframe of errors. 
  
  model <- model
  mean <- mean(cv$residual)
  mspe <- mean(cv$residual^2)
  nmse <- mean(cv$zscore^2)
  cor_ovsp <- cor(cv$observed, cv$observed - cv$residual)
  cor_pvsr <- cor(cv$observed - cv$residual, cv$residual)
  df <- data.frame(model,mean, mspe, nmse, cor_ovsp, cor_pvsr)
  return(df)
}


#Set working director
path <- 'C:/Users/USER/Documents/Kriging Project/'
setwd(path)

#Reading data
#Stations info file
stations_info <- read.csv(file = paste(path, 'Aditional File 1.csv', sep = ''), 
                          encoding = 'UTF-8')
#Area file
area <- read.csv(file = paste(path, 'Area.csv', sep = ''), 
                 encoding = 'UTF-8')
#Rainfall variogram parameters
rainfall_parameters <- read.csv(file = paste(path, 'Rainfall Parameters.csv',
                                             sep = ''), fileEncoding = 'UTF-8-BOM')
#Hurst variogram parameters
hurst_parameters <-read.csv(file = paste(path, 'Hurst Parameters.csv', sep = ''),
                            fileEncoding = 'UTF-8-BOM')

#Rainfall dataframe
df_rainfall <- stations_info[1:6]
#Hurst dataframe
df_hurst <-  stations_info[c(1:5,7)]

# Coordinates in dataframes
coordinates(df_rainfall) <- ~ Latitude.UTM..m. + Longitude.UTM..m.
coordinates(df_hurst) <- ~ Latitude.UTM..m. + Longitude.UTM..m.
coordinates(area) <- ~ Latitude.UTM..m. + Longitude.UTM..m.

#Kriging for rainfall data

#Exponential variogram
c(kg_exp_plot,var_exp_plot,cv_exp)%<-%kriging(df_rainfall,
                                              substr(rainfall_parameters[1,1], 1, 3),
                                              rainfall_parameters[1,2],
                                              rainfall_parameters[1,3],
                                              rainfall_parameters[1,4],
                                              area)
#Kriging plot
plot(kg_exp_plot)
#Cross validation metrics
cross_validation(cv_exp,substr(rainfall_parameters[1,1], 1, 3))

#Spherical semivariogram
c(kg_sph_plot,var_sph_plot,cv_sph)%<-%kriging(df_rainfall,
                                              substr(rainfall_parameters[3,1], 1, 3),
                                              rainfall_parameters[3,2],
                                              rainfall_parameters[3,3],
                                              rainfall_parameters[3,4],
                                              area)
#Kriging plot
plot(kg_sph_plot)
#Cross validation metrics
cross_validation(cv_sph,substr(rainfall_parameters[3,1], 1, 3))

#Hurst data

#Exponential semivariogram
c(kg_exp_plot,var_exp_plot,cv_exp)%<-%kriging(df_hurst,
                                              substr(hurst_parameters[1,1], 1, 3),
                                              hurst_parameters[1,2],
                                              hurst_parameters[1,3],
                                              hurst_parameters[1,4],
                                              area)
#Kriging plot
plot(kg_exp_plot)
#Cross validation metrics
cross_validation(cv_exp,substr(hurst_parameters[1,1], 1, 3))

#Spherical semivariogram
c(kg_sph_plot,var_sph_plot,cv_sph)%<-%kriging(df_hurst,
                                              substr(hurst_parameters[3,1], 1, 3),
                                              hurst_parameters[3,2],
                                              hurst_parameters[3,3],
                                              hurst_parameters[3,4],
                                              area)
#Kriging plot
plot(kg_sph_plot)
#Cross validation metrics
cross_validation(cv_sph,substr(hurst_parameters[3,1], 1, 3))