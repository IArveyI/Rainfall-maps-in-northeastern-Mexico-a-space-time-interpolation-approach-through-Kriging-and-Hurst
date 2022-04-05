#step 2 - Homogenization by Climatol package

#Install package
install.packages('climatol')
#Import libraries
library(climatol)

#Set working directory
setwd('C:/Users/USER/Documents/Kriging Project/Climatol/')

#Homogeneization and interplation of data
homogen('Rmon', 1998, 2018, std=3)
#Data corrected
dahstat('Rmon',1998,2018, stat='series')
