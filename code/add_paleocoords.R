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
  num_coll = length(coll_dat)
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

#Once all replicates are done (i.e. once you have ...chunk6.csv) continue with below

## Load in databases for 30 replicates
## Load in latitude dataframes
lat_chunk1 <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/Paleocoordinates/30Reps/14_02_23_FINSColl_paleolatitudes_V4_chunk1_take2.csv', 
                       header = TRUE)
lat_chunk2 <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/Paleocoordinates/30Reps/14_02_23_FINSColl_paleolatitudes_V4_chunk2.csv', 
                       header = TRUE)
lat_chunk3 <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/Paleocoordinates/30Reps/14_02_23_FINSColl_paleolatitudes_V4_chunk3.csv', 
                       header = TRUE)
lat_chunk4 <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/Paleocoordinates/30Reps/14_02_23_FINSColl_paleolatitudes_V4_chunk4.csv', 
                       header = TRUE)
lat_chunk5 <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/Paleocoordinates/30Reps/14_02_23_FINSColl_paleolatitudes_V4_chunk5.csv', 
                       header = TRUE)
lat_chunk6 <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/Paleocoordinates/30Reps/14_02_23_FINSColl_paleolatitudes_V4_chunk6.csv', 
                       header = TRUE)

## Load in longitude dataframes
lon_chunk1 <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/Paleocoordinates/30Reps/14_02_23_FINSColl_paleolongitude_V4_chunk1_take2.csv', 
                       header = TRUE)
lon_chunk2 <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/Paleocoordinates/30Reps/14_02_23_FINSColl_paleolongitude_V4_chunk2.csv', 
                       header = TRUE)
lon_chunk3 <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/Paleocoordinates/30Reps/14_02_23_FINSColl_paleolongitude_V4_chunk3.csv', 
                       header = TRUE)
lon_chunk4 <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/Paleocoordinates/30Reps/14_02_23_FINSColl_paleolongitude_V4_chunk4.csv', 
                       header = TRUE)
lon_chunk5 <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/Paleocoordinates/30Reps/14_02_23_FINSColl_paleolongitude_V4_chunk5.csv', 
                       header = TRUE)
lon_chunk6 <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/Paleocoordinates/30Reps/14_02_23_FINSColl_paleolongitude_V4_chunk6.csv', 
                       header = TRUE)


## Combine all latitudes into one dataframe
df_30rep_lats <- lat_chunk1
df_30rep_lats <- cbind(df_30rep_lats, lat_chunk2[,7:11])
df_30rep_lats <- cbind(df_30rep_lats, lat_chunk3[,7:11])
df_30rep_lats <- cbind(df_30rep_lats, lat_chunk4[,7:11])
df_30rep_lats <- cbind(df_30rep_lats, lat_chunk5[,7:11])
df_30rep_lats <- cbind(df_30rep_lats, lat_chunk6[,7:11])

## Combine all longitudes into one dataframe
df_30rep_lons <- lon_chunk1
df_30rep_lons <- cbind(df_30rep_lons, lon_chunk2[,7:11])
df_30rep_lons <- cbind(df_30rep_lons, lon_chunk3[,7:11])
df_30rep_lons <- cbind(df_30rep_lons, lon_chunk4[,7:11])
df_30rep_lons <- cbind(df_30rep_lons, lon_chunk5[,7:11])
df_30rep_lons <- cbind(df_30rep_lons, lon_chunk6[,7:11])

## Run coordinate reconstruction function 
dems <- fetch(dat="paleomap", var="dem")
demord <- matchtime(dems, epochs$midpoint)

for (rep in 7:36) {
  #column <- rep - 95
  for (ind in 1:num_coll) {
    tryCatch({
      if (is.na(df_30rep_lats[ind,rep]) == TRUE & is.na(df_30rep_lons[ind,rep]) == TRUE) {
        paleo_lon_lat <- reconstruct(coll_random_ages[ind, c(3,2)], 
                                     age = coll_random_ages[ind,rep], 
                                     enumerate = FALSE, 
                                     model = 'PALEOMAP')
        
        df_30rep_lats[ind,rep] <- paleo_lon_lat[1,2]
        df_30rep_lons[ind,rep] <- paleo_lon_lat[1,1]
        
        print(paste0('PALEOMAP replicate ', rep, ' of collection ', ind))
      }
      on.exit(close(paleo_lon_lat))
    }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
  }
}

print('finished paleocoordinates with PALEOMAP model')


## Check manually if any are still missing coordinates
for (rep in 10:10) {
  for (ind in 1:num_coll) {
    if (is.na(df_30rep_lats[ind,rep]) == TRUE & is.na(df_30rep_lons[ind,rep]) == TRUE) {
      print(df_30rep_lats[ind,1])
    }
  }
}

## Collections consistently missing coordinates
## PBDB_208366 -- lat lon = -57.605278  -63.877777, age = 72.1  66
## PBDB_219778 -- lat lon = 33.393333 -77.148888, age = 5.333 3.6
## PBDB_65985 -- lat lon = 32.900002  -118.5, age = 23.03 5.333
## PBDB_68313 -- lat lon = -18.450001 178.483337, age = 15.97 11.63
## PBDB_68314 -- lat lon = -18.450001 178.483337, age = 15.97 11.63
## PG_1189 -- lat lon = 7.348133333 -80.35218889, age = 37.8  33.9
## PG_1190 -- lat lon = 7.347391667 -80.35374167, age = 37.8  33.9


## Manually fix any if necessary --> MEDIAN AGES ROUNDED TO WHOLE NUMBERS
#print(df_30rep_lons[2862,])

df_30rep_lats[1088,7:36] <- -62.1877
df_30rep_lons[1088,9] <- -61.5042 ## Calculated using median age and Seton 2012 model

df_30rep_lats[1559,9] <- 33.1314
df_30rep_lons[1559,9] <- -76.2667 ## Calculated using median age and Seton 2012 model

df_30rep_lats[2239,c(8, 9, 10, 11, 14, 16, 17, 18, 19, 21, 22, 23, 25, 
                     26, 27, 28, 29, 32, 33, 34, 35, 36)] <- 30.3768
df_30rep_lons[2239, c(8, 9, 10, 11, 14, 16, 17, 18, 19, 21, 22, 23, 25, 
                      26, 27, 28, 29, 32, 33, 34, 35, 36)] <- -112.3613 ## Seton 2012 model. Started with median age and decreased by 1Ma steps until I got result at 10Ma

df_30rep_lats[2262, 7:36] <- -22.78
df_30rep_lons[2262, 7:36] <- 176.8597 ## Calculated using median age and Seton 2012 model

df_30rep_lats[2263, 7:36] <- -22.78
df_30rep_lons[2263, 7:36] <- 176.8597 ## Calculated using median age and Seton 2012 model

df_30rep_lats[2862,7:36] <- 3.8986
df_30rep_lons[2862,7:36] <- -83.7838
## Calculated using Muller 2019. 
## Started with median age and Seton 2012, and decrease age by 1Ma each step until I got 10Ma below minimum age in range
## then switched models to Muller 2019 and repeated process

df_30rep_lats[2864,7:36] <- 3.8986
df_30rep_lons[2864,7:36] <- -83.7838
## Calculated using Muller 2019. 
## Started with median age and Seton 2012, and decrease age by 1Ma each step until I got 10Ma below minimum age in range
## then switched models to Muller 2019 and repeated process

#closeAllConnections()

# Rerun loop to check, confirmed no missing coordinates

## Save file
write.csv(df_30rep_lats, file = '22_02_23_FINSColl_30rep_Paleocoord_lats.csv')
write.csv(df_30rep_lons, file = '22_02_23_FINSColl_30rep_Paleocoord_lons.csv')


#### ASSIGN OCEAN BASINS FROM THE PALEOLATITUDES AND LONGITUDES ####

## Create a dataframe to store the epochs
df_epoch <- data.frame(matrix(data = NA, nrow=num_coll, ncol=36))  # 7:106 total, 7:16 for 10 sets of 10 reps
rownames(df_epoch) <- coll_dat$collection_number
colnames(df_epoch) <- column_names
df_epoch$coll_num <- coll_dat$collection_number
df_epoch$lat <- coll_dat$lat
df_epoch$lon <- coll_dat$lon
df_epoch$cell <- coll_random_ages$cell
df_epoch$centerlon <- coll_random_ages$centerlon
df_epoch$centerlat <- coll_random_ages$centerlat

print('begin assinging epochs')
## Assign epoch
for (ind in 7:36) {  # 7:106 total, 7:16 for 10 sets of 10 reps
  column <- ind
  for (coll in 1:num_coll) {
    print(paste0('epoch replicate ', ind, ' of collection ', coll))
    if (coll_random_ages[coll, ind] <= epochs[1,2] && coll_random_ages[coll,ind] > epochs[1,3]) {
      df_epoch[coll,column] <- 'Lower Jurassic'
    }
    else if (coll_random_ages[coll, ind] <= epochs[2,2] && coll_random_ages[coll,ind] > epochs[2,3]) {
      df_epoch[coll,column] <- 'Middle Jurassic'
    }
    else if (coll_random_ages[coll, ind] <= epochs[3,2] && coll_random_ages[coll,ind] > epochs[3,3]) {
      df_epoch[coll,column] <- 'Upper Jurassic'
    }
    else if (coll_random_ages[coll,ind] <= epochs[4,2] && coll_random_ages[coll,ind] > epochs[4,3]) {
      df_epoch[coll,column] <- 'Lower Cretaceous'
    }
    else if (coll_random_ages[coll,ind] <= epochs[5,2] && coll_random_ages[coll,ind] > epochs[5,3]) {
      df_epoch[coll,column] <- 'Upper Cretaceous'
    }
    else if (coll_random_ages[coll,ind] <= epochs[6,2] && coll_random_ages[coll,ind] > epochs[6,3]) {
      df_epoch[coll,column] <- 'Paleocene'
    }
    else if (coll_random_ages[coll,ind] <= epochs[7,2] && coll_random_ages[coll,ind] > epochs[7,3]) {
      df_epoch[coll,column] <- 'Eocene'
    }
    else if (coll_random_ages[coll,ind] <= epochs[8,2] && coll_random_ages[coll,ind] > epochs[8,3]) {
      df_epoch[coll,column] <- 'Oligocene'
    }
    else if (coll_random_ages[coll,ind] <= epochs[9,2] && coll_random_ages[coll,ind] > epochs[9,3]) {
      df_epoch[coll,column] <- 'Miocene'
    }
    else if (coll_random_ages[coll,ind] <= epochs[10,2] && coll_random_ages[coll,ind] > epochs[10,3]) {
      df_epoch[coll,column] <- 'Pliocene'
    }
    else if (coll_random_ages[coll,ind] <= epochs[11,2] && coll_random_ages[coll,ind] > epochs[11,3]) {
      df_epoch[coll,column] <- 'Pleistocene'
    }
    else if (coll_random_ages[coll,ind] <= epochs[12,2] && coll_random_ages[coll,ind] > epochs[12,3]) {
      df_epoch[coll,column] <- 'Holocene'
    }
    else if (coll_random_ages[coll,ind] == 0) {
      df_epoch[coll,column] <- 'Holocene'
    }
  }
}
print('finished epcoh assignment')

write.csv(df_epoch, file = "./2_02_23_FINSColl_30rep_Epoch.csv", row.names = FALSE)

## Create dataframe to store ocean basins 
df_ocean_basins <- data.frame(matrix(data = NA, nrow=num_coll, ncol=36))  # 7:106 total, 7:16 for 10 sets of 10 reps
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
for (rep in 7:30) {  # 7:106 total, 7:16 for 10 sets of 10 reps
  for (ind in 1:num_coll) {
    print(paste0('ocean basin replicate ', rep, ' of collection ', ind))
    if(is.na(df_30rep_lats[ind,rep]) && is.na(df_30rep_lons[ind,rep])) next
    #if (is.na(df_30rep_lats[ind,rep]) == FALSE && is.na(df_30rep_lons[ind,rep]) == FALSE) {
    if (df_epoch[ind,rep] == 'Lower Cretaceous') {
      if (df_30rep_lons[ind,rep] < -30 && df_30rep_lons[ind,rep] > -70 && df_30rep_lats[ind,rep] > 30 && df_30rep_lats[ind,rep] < 70) {
        df_ocean_basins[ind,rep] <-'Western Interior Seaway'
      }
      else if (df_30rep_lons[ind,rep] > 30 && df_30rep_lons[ind,rep] < 120 && df_30rep_lats[ind,rep] < 30 && df_30rep_lats[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Tethys'
      }
      else if (df_30rep_lons[ind,rep] < 0 && df_30rep_lons[ind,rep] > -50 && df_30rep_lats[ind,rep] > 0 && df_30rep_lats[ind,rep] < 40) {
        df_ocean_basins[ind,rep] <-'Western Tethys'
      }
      else if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 30 && df_30rep_lats[ind,rep] > 0 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Tethys Seaway'
      }
      else if (df_30rep_lons[ind,rep] > 30 && df_30rep_lons[ind,rep] < 60 && df_30rep_lats[ind,rep] > 30 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Tethys Seaway'
      }
      else if (df_30rep_lons[ind,rep] < 0 && df_30rep_lons[ind,rep] > -30 && df_30rep_lats[ind,rep] < 0 && df_30rep_lats[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (df_30rep_lons[ind,rep] < -40 && df_30rep_lons[ind,rep] > -55 && df_30rep_lats[ind,rep] < 0 && df_30rep_lats[ind,rep] > -20) {
        df_ocean_basins[ind,rep] <-'South American Epicontinental Seas'
      }
      else if (df_30rep_lats[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Upper Cretaceous') {
      if (df_30rep_lons[ind,rep] > 30 && df_30rep_lons[ind,rep] < 120 && df_30rep_lats[ind,rep] < 30 && df_30rep_lats[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Tethys'
      }
      else if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 30 && df_30rep_lats[ind,rep] > -15 && df_30rep_lats[ind,rep] < 15) {
        df_ocean_basins[ind,rep] <-'Trans-Saharan Seaway'
      }
      else if (df_30rep_lons[ind,rep] < 0 && df_30rep_lons[ind,rep] > -60 && df_30rep_lats[ind,rep] > 0 && df_30rep_lats[ind,rep] < 40) {
        df_ocean_basins[ind,rep] <-'Western Tethys'
      }
      else if (df_30rep_lons[ind,rep] < -30 && df_30rep_lons[ind,rep] > -50 && df_30rep_lats[ind,rep] > 30 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Western Interior Seaway'
      }
      else if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 30 && df_30rep_lats[ind,rep] > 0 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Tethys Seaway'
      }
      else if (df_30rep_lons[ind,rep] > 30 && df_30rep_lons[ind,rep] < 60 && df_30rep_lats[ind,rep] > 30 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Tethys Seaway'
      }
      else if (df_30rep_lons[ind,rep] < 0 && df_30rep_lons[ind,rep] > -30 && df_30rep_lats[ind,rep] < 0 && df_30rep_lats[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (df_30rep_lons[ind,rep] < -40 && df_30rep_lons[ind,rep] > -55 && df_30rep_lats[ind,rep] < 0 && df_30rep_lats[ind,rep] > -25) {
        df_ocean_basins[ind,rep] <-'South American Epicontinental Seas'
      }
      else if (df_30rep_lats[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Paleocene') {
      if (df_30rep_lons[ind,rep] < 0 && df_30rep_lons[ind,rep] > 60 && df_30rep_lats[ind,rep] > 0 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (df_30rep_lons[ind,rep] < 5 && df_30rep_lons[ind,rep] > -45 && df_30rep_lats[ind,rep] < 0 && df_30rep_lats[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 120 && df_30rep_lats[ind,rep] < 60 && df_30rep_lats[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Tethys'
      }
      else if (df_30rep_lats[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <- 'Arctic'
      }
      else if (df_30rep_lats[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Eocene') {
      if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 120 && df_30rep_lats[ind,rep] < 0 && df_30rep_lats[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Indian'
      }
      else if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 120 && df_30rep_lats[ind,rep] > 0 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Neo-Tethys'
      }
      else if (df_30rep_lons[ind,rep] < 0 && df_30rep_lons[ind,rep] > -60 && df_30rep_lats[ind,rep] > -60 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (df_30rep_lats[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else if (df_30rep_lats[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Oligocene') {
      if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 45 && df_30rep_lats[ind,rep] > 22.5 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Neo-Tethys'
      }
      else if (df_30rep_lons[ind,rep] < 0 && df_30rep_lons[ind,rep] > -60 && df_30rep_lats[ind,rep] > -60 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (df_30rep_lons[ind,rep] > 30 && df_30rep_lons[ind,rep] < 120 && df_30rep_lats[ind,rep] < 15 && df_30rep_lats[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Indian'
      }
      else if (df_30rep_lats[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <- 'Arctic'
      }
      else if (df_30rep_lats[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Miocene') {
      if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 45 && df_30rep_lats[ind,rep] > 22.5 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Neo-Tethys'
      }
      else if (df_30rep_lons[ind,rep] < 0 && df_30rep_lons[ind,rep] > -60 && df_30rep_lats[ind,rep] > -60 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (df_30rep_lons[ind,rep] > 30 && df_30rep_lons[ind,rep] < 120 && df_30rep_lats[ind,rep] < 15 && df_30rep_lats[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Indian'
      }
      else if (df_30rep_lats[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else if (df_30rep_lats[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Pliocene') {
      if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 45 && df_30rep_lats[ind,rep] > 22.5 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Mediterranean'
      }
      else if (df_30rep_lons[ind,rep] < 0 && df_30rep_lons[ind,rep] > -60 && df_30rep_lats[ind,rep] > -60 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (df_30rep_lons[ind,rep] > 30 && df_30rep_lons[ind,rep] < 120 && df_30rep_lats[ind,rep] < 20 && df_30rep_lats[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Indian'
      }
      else if (df_30rep_lats[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else if (df_30rep_lats[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    } 
    else if (df_epoch[ind,rep] == 'Pleistocene') {
      if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 45 && df_30rep_lats[ind,rep] > 22.5 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Mediterranean'
      }
      else if (df_30rep_lons[ind,rep] < 0 && df_30rep_lons[ind,rep] > -60 && df_30rep_lats[ind,rep] > -60 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (df_30rep_lons[ind,rep] > 30 && df_30rep_lons[ind,rep] < 120 && df_30rep_lats[ind,rep] < 20 && df_30rep_lats[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Indian'
      }
      else if (df_30rep_lats[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else if (df_30rep_lats[ind,rep] < -60) {
        df_ocean_basins[ind,rep] <-'Southern'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    } 
    else if (df_epoch[ind,rep] == 'Holocene') {
      if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 45 && df_30rep_lats[ind,rep] > 22.5 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Mediterranean'
      }
      else if (df_30rep_lons[ind,rep] < 0 && df_30rep_lons[ind,rep] > -60 && df_30rep_lats[ind,rep] > -60 && df_30rep_lats[ind,rep] < 60) {
        df_ocean_basins[ind,rep] <-'Atlantic'
      }
      else if (df_30rep_lons[ind,rep] > 30 && df_30rep_lons[ind,rep] < 120 && df_30rep_lats[ind,rep] < 20 && df_30rep_lats[ind,rep] > -60) {
        df_ocean_basins[ind,rep] <-'Indian'
      }
      else if (df_30rep_lats[ind,rep] > 60) {
        df_ocean_basins[ind,rep] <-'Arctic'
      }
      else if (df_30rep_lats[ind,rep] < -60) {
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

print('saving ocean basins')
write.csv(df_ocean_basins, file = './22_02_23_FINSColl_Paleo_Coordinates_30rep_Ocean.csv', row.names = FALSE)

## Find the mode of Ocean Basin and Paleo-Coordinates for each collection and add it to dataframe
df_paleoinfo <- data.frame(matrix(data = NA, nrow = num_coll, ncol = 4))
colnames(df_paleoinfo) <- c('coll_name', 'paleolat', 'paleolon', 'paleoocean')

df_paleoinfo$coll_name <- coll_dat$collection_number


for (col in 1:num_coll) {
  mode_lat <- apply(df_30rep_lats[col, 7:36], 1, mfv1, na_rm = TRUE)
  mode_lon <- apply(df_30rep_lons[col, 7:36], 1, mfv1, na_rm = TRUE)
  mode_ocean <- apply(df_ocean_basins[col, 7:36], 1, mfv1, na_rm = TRUE)
  
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

write.csv(df_paleoinfo, file = './22_02_23_FINSColl_Paleo_Coordinates_30rep_Modes.csv', row.names = FALSE)


#### Assign Ocean Basins to each occurrence based on what collection it belongs to ####
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

write.csv(occ_df, file = "./22_02_23_FINSOccs_Paleo_Coordinates_30reps_Modes.csv", row.names = FALSE)

print('done with occurrence dataframe')



