#Step 3 - Hurst exponent and mean rainfall

#Install packages
install.packages('pracma')
install.packages('dplyr')
#Import libraries
library(pracma)
library(dplyr)
#Functions

hurst<-function(df){
  
  #hurst make a dataframe of hurst values giving a time serie dataframe.
  
  #:param df: Dataframe of time series of each point.0
  #:return hurst_data: Dataframe of hurst exponent of each point. 
  
  all_hurst <- c()
  for(station in 1:nrow(df)) {
    values<-df[station,2:ncol(df)]
    values <- values[!is.na(values)]
    all_hurst[station]<-hurstexp(values, d=24)$Hal
  }
  hurst_data <- data.frame(all_hurst)
  return(hurst_data)
}

#Set working director
path <- 'C:/Users/USER/Documents/Kriging Project/'
setwd(path)

#Reading Data
#Stations Percentage of Original Data file
station_pod <- read.csv(file = paste(path, 'Stations POD.csv', sep = ''), 
                        encoding = 'UTF-8')
colnames(station_pod)[1] <- 'ACmx'
#Stations Info
station_info <- read.csv(file = paste(path, 'Stations Info.csv', sep = ''),
                         encoding = 'UTF-8')
colnames(station_info)[1] <- 'Code'
#Station data
station_data <- read.csv(file = paste(path, 'Climatol/Rmon_1998-2018_series.csv',
                                      sep = ''), encoding = 'UTF-8', header = FALSE)
station_data[1] <- NULL

#Filter by POD >= 80
station_pod <- filter(station_pod, POD >= 80)

station_info <- subset(station_info, 
                       station_info$Station.Name %in% station_pod$Name)
rownames(station_info) <- NULL

#Filtering station data with POD >= 80
station_data <- as.data.frame(t(station_data))
station_pod$C <- formatC(as.numeric(station_pod$C), digits = 1, format = "f")
station_data <- subset(station_data, station_data$V1 %in% station_pod$C)
station_data <- as.data.frame(lapply(station_data, as.numeric))
station_data[station_data<0] <- 0

#Station Mean Annual Rainfall (mm)
rownames(station_data) <- as.numeric(station_data[,1])
station_data[,1] <- NULL
station_info['Annual Rainfall (mm)'] <- rowSums(station_data)/21

#Station Hurst Exponent
station_info['Hurst Exponent'] <- hurst(station_data)

#Saving Aditional File 1
colnames(station_info)[2] <- 'Station Name'
colnames(station_info)[3] <- 'Latitude UTM (m)'
colnames(station_info)[4] <- 'Longitude UTM (m)'
colnames(station_info)[5] <- 'Elevation (masl)'
write.csv(station_info, paste(path, 'Aditional File 1.csv', sep = ''),
          row.names = FALSE)
