"""
Project: FINS Database
Author: Amanda Gardiner
Description:
Addition of paleocoordinates to collections based on modern coordinates, using Mathews 2016 and PALEOMAP (Scotese 2016) models
Addition of paleo-ocean basins based on paleocoordinates
"""

library(dplyr)
library(dggridR)
library(tidyr)
library(chronosphere)
library(readxl)

## Load relavant dataframes

coll_dat <- read_xlsx('/Users/amandagardiner/Dropbox/Analyses/Data/Master\ files/fins.xlsx', 
                 sheet = 'Collections')

coll_random_ages <- read.csv('12_02_23_FINSColl_RandomAge.csv', header = TRUE)

## Load in Epoch, midpoints needed for reconstruction function below
epochs <- data.frame(epoch = c('Lower Cretaceous', 'Upper Cretaceous', 'Paleocene', 'Eocene', 'Oligocene', 'Miocene', 'Pliocene', 'Pleistocene', 'Holocene'), 
                     start = c(145, 100.5, 66, 56, 33.9, 23.03, 5.333, 2.58, 0.0117), 
                     end = c(100.5, 66, 56, 33.9, 23.03, 5.333, 2.58, 0.0117, 0), 
                     midpoint = c(0, 0, 0, 0, 0, 0, 0, 0, 0))
for (i in 1:length(epochs$epoch)) {
  age_vec <- c(epochs[i,2], epochs[i,3])
  mid <- median(age_vec)
  epochs[i,4] <- mid
}


#### PALEOCOORDINATES RECONSTRUCTION ####
### distinct(age, Long_cent, lat_cent)

## Create dataframe to store all paleocoordinates replicates with random ages
## In each round 5 age replicates are used to calculate paleocoords (can't to all 30 at once due to computational restrictions)
## Therefore this process is repeated 6 times (producing ...chunkX.csv), each time shifting the age column indices by 5

## First 6 collumns populated with info from other dataframes
coll_paleocoord_lon <- data.frame(matrix(data = NA, nrow=num_coll, ncol=11))
rownames(coll_paleocoord_lon) <- coll_dat$collection_number
colnames(coll_paleocoord_lon) <- column_names
coll_paleocoord_lon$coll_num <- coll_dat$collection_number
coll_paleocoord_lon$lat <- coll_dat$lat
coll_paleocoord_lon$lon <- coll_dat$lon
coll_paleocoord_lon$cell <- coll_random_ages$cell
coll_paleocoord_lon$centerlon <- coll_random_ages$centerlon
coll_paleocoord_lon$centerlat <- coll_random_ages$centerlat

coll_paleocoord_lat <- data.frame(matrix(data = NA, nrow=num_coll, ncol=11))
rownames(coll_paleocoord_lat) <- coll_dat$collection_number
colnames(coll_paleocoord_lat) <- column_names
coll_paleocoord_lat$coll_num <- coll_dat$collection_number
coll_paleocoord_lat$lat <- coll_dat$lat
coll_paleocoord_lat$lon <- coll_dat$lon
coll_paleocoord_lat$cell <- coll_random_ages$cell
coll_paleocoord_lat$centerlon <- coll_random_ages$centerlon
coll_paleocoord_lat$centerlat <- coll_random_ages$centerlat


## Run coordinate reconstruction function 
dems <- fetch(dat="paleomap", var="dem")
demord <- matchtime(dems, epochs$midpoint)

chunks <- seq(1, num_coll, by = 5) 
print('starting paleocoordinates reconstruction')

for (rep in 7:11) {
  column <- rep
  for (ind in chunks) {
    tryCatch({
      replicate <- rep - 6
      nextrow_two <- ind + 1
      nextrow_three <- ind + 2
      nextrow_four <- ind + 3
      nextrow_five <- ind + 4
      
      if (ind == 5926) {
        paleo_lon_lat <- reconstruct(coll_random_ages[ind:nextrow_four, c(3,2)], # c(5,6) == cell center coordinates
                                     age=c(coll_random_ages[ind,rep], 
                                           coll_random_ages[nextrow_two,rep], 
                                           coll_random_ages[nextrow_three,rep], 
                                           coll_random_ages[nextrow_four,rep] 
                                           ), 
                                     enumerate = FALSE, 
                                     model = 'MATTHEWS2016_mantle_ref')
        
        coll_paleocoord_lat[ind,column] <- paleo_lon_lat[1,2]
        coll_paleocoord_lon[ind,column] <- paleo_lon_lat[1,1]
        
        coll_paleocoord_lat[nextrow_two,column] <- paleo_lon_lat[2,2]
        coll_paleocoord_lon[nextrow_two,column] <- paleo_lon_lat[2,1]
        
        coll_paleocoord_lat[nextrow_three,column] <- paleo_lon_lat[3,2]
        coll_paleocoord_lon[nextrow_three,column] <- paleo_lon_lat[3,1]
        
        coll_paleocoord_lat[nextrow_four,column] <- paleo_lon_lat[4,2]
        coll_paleocoord_lon[nextrow_four,column] <- paleo_lon_lat[4,1]
        
      }
      else {
        paleo_lon_lat <- reconstruct(coll_random_ages[ind:nextrow_five, c(3,2)], # c(5,6) == cell center coordinates
                                     age=c(coll_random_ages[ind,rep], 
                                           coll_random_ages[nextrow_two,rep], 
                                           coll_random_ages[nextrow_three,rep], 
                                           coll_random_ages[nextrow_four,rep], 
                                           coll_random_ages[nextrow_five,rep]
                                           ), 
                                     enumerate = FALSE, 
                                     model = 'MATTHEWS2016_mantle_ref')
        
        coll_paleocoord_lat[ind,column] <- paleo_lon_lat[1,2]
        coll_paleocoord_lon[ind,column] <- paleo_lon_lat[1,1]
        
        coll_paleocoord_lat[nextrow_two,column] <- paleo_lon_lat[2,2]
        coll_paleocoord_lon[nextrow_two,column] <- paleo_lon_lat[2,1]
        
        coll_paleocoord_lat[nextrow_three,column] <- paleo_lon_lat[3,2]
        coll_paleocoord_lon[nextrow_three,column] <- paleo_lon_lat[3,1]
        
        coll_paleocoord_lat[nextrow_four,column] <- paleo_lon_lat[4,2]
        coll_paleocoord_lon[nextrow_four,column] <- paleo_lon_lat[4,1]
        
        coll_paleocoord_lat[nextrow_five,column] <- paleo_lon_lat[5,2]
        coll_paleocoord_lon[nextrow_five,column] <- paleo_lon_lat[5,1]
        
      }
      print(paste0('paleocoordinates replicate ', replicate, ' of collection ', ind))
      on.exit(close(paleo_lon_lat))
    }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
  }
}

print('finished paleocoordinates with Matthew 2016 model')


for (rep in 7:11) {
  column <- rep
  for (ind in 1:num_coll) {
    tryCatch({
      if (is.na(coll_paleocoord_lat[ind, rep]) == TRUE & is.na(coll_paleocoord_lon[ind,rep]) == TRUE ) {
        paleo_lon_lat <- reconstruct(coll_random_ages[ind, c(3,2)], 
                                     age = coll_random_ages[ind,rep], 
                                     enumerate = FALSE, 
                                     model = 'PALEOMAP')
        
        coll_paleocoord_lat[ind,column] <- paleo_lon_lat[1,2]
        coll_paleocoord_lon[ind,column] <- paleo_lon_lat[1,1]
        
      }
      on.exit(close(paleo_lon_lat))
      print(paste0('PALEOMAP replicate ', rep, ' of collection ', ind))
    }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
  }
}

print('finished paleocoordinates with PALEOMAP model')

## Save paleocoordinates to csv
print('saving paleocoordinates')
write.csv(coll_paleocoord_lat, file = './14_02_23_FINSColl_paleolatitudes_V4_chunk1.csv', row.names = FALSE)
write.csv(coll_paleocoord_lon, file = './14_02_23_FINSColl_paleolongitude_V4_chunk1.csv', row.names = FALSE)
print('finished saving paleocoordinates')



## Identify ocean basins using the replicates of ages and paleocoords, again repeat 6 times with sets of 5 replicates

## Create dataframe to store ocean basins 
df_ocean_basins <- data.frame(matrix(data = NA, nrow=num_coll, ncol=11))
rownames(df_ocean_basins) <- coll_dat$collection_number
colnames(df_ocean_basins) <- column_names
df_ocean_basins$coll_num <- coll_dat$collection_number
df_ocean_basins$lat <- coll_dat$lat
df_ocean_basins$lon <- coll_dat$lon
df_ocean_basins$cell <- coll_random_ages$cell
df_ocean_basins$centerlon <- coll_random_ages$centerlon
df_ocean_basins$centerlat <- coll_random_ages$centerlat

print('starting ocean basin assignment')
## Assign ocean basin based on paleocoord and age
for (rep in 7:11) {  # 7:106 total, 7:16 for 10 sets of 10 reps
  for (ind in 1:num_coll) {
    print(paste0('ocean basin replicate ', rep, ' of collection ', ind))
    if(is.na(coll_paleocoord_lat[ind,rep]) && is.na(coll_paleocoord_lon[ind,rep])) next
    #if (is.na(coll_paleocoord_lat[ind,rep]) == FALSE && is.na(coll_paleocoord_lon[ind,rep]) == FALSE) {
	if (df_epoch[ind,rep] == 'Lower Cretaceous') {
      if (coll_paleocoord_lon[ind,rep] < -30 && coll_paleocoord_lon[ind,rep] > -70 && coll_paleocoord_lat[ind,rep] > 30 && coll_paleocoord_lat[ind,rep] < 70) {
        df_ocean_basins[ind,rep] <-'Western Interior Seaway'
      }
      else if (coll_paleocoord_lon[ind,rep] > 30 && coll_paleocoord_lon[ind,rep] < 120 && coll_paleocoord_lat[ind,rep] < 30 && coll_paleocoord_lat[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Tethys'
      }
      else if (coll_paleocoord_lon[ind,rep] < 0 && coll_paleocoord_lon[ind,rep] > -50 && coll_paleocoord_lat[ind,rep] > 0 && coll_paleocoord_lat[ind,rep] < 40) {
        df_ocean_basins[ind,rep] <-'Western Tethys'
      }
      else if (coll_paleocoord_lon[ind,rep] > 0 && coll_paleocoord_lon[ind,rep] < 30 && coll_paleocoord_lat[ind,rep] > 0 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Tethys Seaway'
      }
      else if (coll_paleocoord_lon[ind,rep] > 30 && coll_paleocoord_lon[ind,rep] < 60 && coll_paleocoord_lat[ind,rep] > 30 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Tethys Seaway'
      }
      else if (coll_paleocoord_lon[ind,rep] < 0 && coll_paleocoord_lon[ind,rep] > -30 && coll_paleocoord_lat[ind,rep] < 0 && coll_paleocoord_lat[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (coll_paleocoord_lon[ind,rep] < -40 && coll_paleocoord_lon[ind,rep] > -55 && coll_paleocoord_lat[ind,rep] < 0 && coll_paleocoord_lat[ind,rep] > -20) {
        df_ocean_basins[ind,rep] <-'South American Epicontinental Seas'
      }
      else if (coll_paleocoord_lat[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Upper Cretaceous') {
      if (coll_paleocoord_lon[ind,rep] > 30 && coll_paleocoord_lon[ind,rep] < 120 && coll_paleocoord_lat[ind,rep] < 30 && coll_paleocoord_lat[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Tethys'
      }
      else if (coll_paleocoord_lon[ind,rep] > 0 && coll_paleocoord_lon[ind,rep] < 30 && coll_paleocoord_lat[ind,rep] > -15 && coll_paleocoord_lat[ind,rep] < 15) {
        df_ocean_basins[ind,rep] <-'Trans-Saharan Seaway'
      }
      else if (coll_paleocoord_lon[ind,rep] < 0 && coll_paleocoord_lon[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] > 0 && coll_paleocoord_lat[ind,rep] < 40) {
        df_ocean_basins[ind,rep] <-'Western Tethys'
      }
      else if (coll_paleocoord_lon[ind,rep] < -30 && coll_paleocoord_lon[ind,rep] > -50 && coll_paleocoord_lat[ind,rep] > 30 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Western Interior Seaway'
      }
      else if (coll_paleocoord_lon[ind,rep] > 0 && coll_paleocoord_lon[ind,rep] < 30 && coll_paleocoord_lat[ind,rep] > 0 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Tethys Seaway'
      }
      else if (coll_paleocoord_lon[ind,rep] > 30 && coll_paleocoord_lon[ind,rep] < 60 && coll_paleocoord_lat[ind,rep] > 30 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Tethys Seaway'
      }
      else if (coll_paleocoord_lon[ind,rep] < 0 && coll_paleocoord_lon[ind,rep] > -30 && coll_paleocoord_lat[ind,rep] < 0 && coll_paleocoord_lat[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (coll_paleocoord_lon[ind,rep] < -40 && coll_paleocoord_lon[ind,rep] > -55 && coll_paleocoord_lat[ind,rep] < 0 && coll_paleocoord_lat[ind,rep] > -25) {
        df_ocean_basins[ind,rep] <-'South American Epicontinental Seas'
      }
      else if (coll_paleocoord_lat[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Paleocene') {
      if (coll_paleocoord_lon[ind,rep] < 0 && coll_paleocoord_lon[ind,rep] > 60 && coll_paleocoord_lat[ind,rep] > 0 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (coll_paleocoord_lon[ind,rep] < 5 && coll_paleocoord_lon[ind,rep] > -45 && coll_paleocoord_lat[ind,rep] < 0 && coll_paleocoord_lat[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (coll_paleocoord_lon[ind,rep] > 0 && coll_paleocoord_lon[ind,rep] < 120 && coll_paleocoord_lat[ind,rep] < 60 && coll_paleocoord_lat[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Tethys'
      }
      else if (coll_paleocoord_lat[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <- 'Arctic'
      }
      else if (coll_paleocoord_lat[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Eocene') {
      if (coll_paleocoord_lon[ind,rep] > 0 && coll_paleocoord_lon[ind,rep] < 120 && coll_paleocoord_lat[ind,rep] < 0 && coll_paleocoord_lat[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Indian'
      }
      else if (coll_paleocoord_lon[ind,rep] > 0 && coll_paleocoord_lon[ind,rep] < 120 && coll_paleocoord_lat[ind,rep] > 0 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Neo-Tethys'
      }
      else if (coll_paleocoord_lon[ind,rep] < 0 && coll_paleocoord_lon[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (coll_paleocoord_lat[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else if (coll_paleocoord_lat[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Oligocene') {
      if (coll_paleocoord_lon[ind,rep] > 0 && coll_paleocoord_lon[ind,rep] < 45 && coll_paleocoord_lat[ind,rep] > 22.5 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Neo-Tethys'
      }
      else if (coll_paleocoord_lon[ind,rep] < 0 && coll_paleocoord_lon[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (coll_paleocoord_lon[ind,rep] > 30 && coll_paleocoord_lon[ind,rep] < 120 && coll_paleocoord_lat[ind,rep] < 15 && coll_paleocoord_lat[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Indian'
      }
      else if (coll_paleocoord_lat[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <- 'Arctic'
      }
      else if (coll_paleocoord_lat[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Miocene') {
      if (coll_paleocoord_lon[ind,rep] > 0 && coll_paleocoord_lon[ind,rep] < 45 && coll_paleocoord_lat[ind,rep] > 22.5 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Neo-Tethys'
      }
      else if (coll_paleocoord_lon[ind,rep] < 0 && coll_paleocoord_lon[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (coll_paleocoord_lon[ind,rep] > 30 && coll_paleocoord_lon[ind,rep] < 120 && coll_paleocoord_lat[ind,rep] < 15 && coll_paleocoord_lat[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Indian'
      }
      else if (coll_paleocoord_lat[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else if (coll_paleocoord_lat[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Pliocene') {
      if (coll_paleocoord_lon[ind,rep] > 0 && coll_paleocoord_lon[ind,rep] < 45 && coll_paleocoord_lat[ind,rep] > 22.5 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Mediterranean'
      }
      else if (coll_paleocoord_lon[ind,rep] < 0 && coll_paleocoord_lon[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (coll_paleocoord_lon[ind,rep] > 30 && coll_paleocoord_lon[ind,rep] < 120 && coll_paleocoord_lat[ind,rep] < 20 && coll_paleocoord_lat[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Indian'
      }
      else if (coll_paleocoord_lat[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else if (coll_paleocoord_lat[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    } 
    else if (df_epoch[ind,rep] == 'Pleistocene') {
      if (coll_paleocoord_lon[ind,rep] > 0 && coll_paleocoord_lon[ind,rep] < 45 && coll_paleocoord_lat[ind,rep] > 22.5 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Mediterranean'
      }
      else if (coll_paleocoord_lon[ind,rep] < 0 && coll_paleocoord_lon[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (coll_paleocoord_lon[ind,rep] > 30 && coll_paleocoord_lon[ind,rep] < 120 && coll_paleocoord_lat[ind,rep] < 20 && coll_paleocoord_lat[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Indian'
      }
      else if (coll_paleocoord_lat[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else if (coll_paleocoord_lat[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    } 
    else if (df_epoch[ind,rep] == 'Holocene') {
      if (coll_paleocoord_lon[ind,rep] > 0 && coll_paleocoord_lon[ind,rep] < 45 && coll_paleocoord_lat[ind,rep] > 22.5 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Mediterranean'
      }
      else if (coll_paleocoord_lon[ind,rep] < 0 && coll_paleocoord_lon[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] > -60 && coll_paleocoord_lat[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (coll_paleocoord_lon[ind,rep] > 30 && coll_paleocoord_lon[ind,rep] < 120 && coll_paleocoord_lat[ind,rep] < 20 && coll_paleocoord_lat[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Indian'
      }
      else if (coll_paleocoord_lat[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else if (coll_paleocoord_lat[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    #}
  }
}

print('finish assigning ocean basins')

## Find the mode of Ocean Basin and Paleo-Coordinates for each collection and add it to dataframe
df_paleoinfo <- data.frame(matrix(data = NA, nrow = num_coll, ncol = 4))
colnames(df_paleoinfo) <- c('coll_name', 'paleolat', 'paleolon', 'paleoocean')

df_paleoinfo$coll_name <- coll_dat$collection_number


for (col in 1:num_coll) {
  mode_lat <- apply(coll_paleocoord_lat[col, 7:11], 1, mfv1, na_rm = TRUE)
  mode_lon <- apply(coll_paleocoord_lon[col, 7:11], 1, mfv1, na_rm = TRUE)
  mode_ocean <- apply(df_ocean_basins[col, 7:11], 1, mfv1, na_rm = TRUE)
  
  df_paleoinfo[col, 2] <- round(as.numeric(mode_lat), digits = 2)
  df_paleoinfo[col, 3] <- round(as.numeric(mode_lon), digits = 2)
  if (mode_lat == '' && mode_lon == '') {
    df_paleoinfo[col, 4] <- ''
  }
  else {
    df_paleoinfo[col, 4] <- mode_ocean
  }
  print(paste0('Collection ', col, ' of ', num_coll, ' done'))
}

print('finish assigning modes')

write.csv(df_paleoinfo, file = './14_02_23_FINSColl_Paleo_Coordinates_Oceans_V4_chunk1.csv', row.names = FALSE)


#### Assign Ocean Basins to each occurrence based on what collection it belongs to 
num_occ <- length(occ_dat$occurrence_number)

occ_df <- data.frame(matrix(data = NA, nrow = num_occ, ncol = 5))
colnames(occ_df) <- c('coll_num', 'occ_num', 'paleolat',  'paleolon', 'ocean')

for (ind in 1:num_occ) {
  occ_df[ind,1] <- occ_dat[ind, 3]
  occ_df[ind,2] <- occ_dat[ind, 1]
}

for (ind in 1:num_occ) {
  for (coll in 1:num_coll) {
    if (occ_df[ind,1] == df_paleoinfo[coll,1]) {
      occ_df[ind, 3] <- df_paleoinfo[coll, 2]
      occ_df[ind, 4] <- df_paleoinfo[coll, 3]
      occ_df[ind, 5] <- df_paleoinfo[coll, 4]
      print(paste0('Matched Occurrence ', ind))
    }
  }
}

write.csv(occ_df, file = "./14_02_23_FINSOccs_Paleo_Coordinates_Oceans_V4_chunk1.csv", row.names = FALSE)

print('done with occurrence dataframe')

