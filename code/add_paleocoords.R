#### GOAL: Implement Raster Cells over earth to do paleocoordinates ####
## V4
## Test worked -- now implement for whole database and add paleo-ocean categorization script
## Code to generate age replicates and cell coordinates worked but the paleocoordinates take too long to run in a row
## Broke up into 10 scripts, each of which generates paleocoordinates for 10 sets of replicates
### Then broke UP INTO 20 SCRIPTS, EACH OF WHICH FOR 5 SETS OF REPLICATES
### NOW Doing single replicate at a time on my computer
## 10.02.23
## Author: Amanda Gardiner
## Partition the earth into equal area grids
## Bin all collections into raster grids
####

## Library necessary packages
library(dplyr)
library(dggridR)
library(tidyr)

#### MODIFIED 20250308 ####
library(raster)
library(terra)
require(remotes)
install_version("chronosphere", version = "0.4.1", repos = "http://cran.us.r-project.org")
library(ncdf4)
####

library(chronosphere)

library(readxl)
library(ggplot2)
print('finished loading packages')

## Load in database
print('loading databases')

### ADD EACH COLLECTION TO 30 RANDOMLY REPLICATES CELLS BASED ON MODERN COORDINATES AND AGE

# Load in data
coll_dat <- read_xlsx('/Users/kristinakocakova/Dropbox/Analyses/Data/Master\ files/colls_added_March_2025.xlsx')

num_coll <- length(coll_dat$collection_number)

## ASSIGN EACH COLL. TO A GRID CELL ##
## Construct a global grid with cells approximately 2000 km across
dggs <- dgconstruct(spacing=1000, metric=TRUE, resround='down')


## Create dataframe to store all information and randomly selected ages for each collection
coll_random_ages <- data.frame(matrix(data = NA, nrow=num_coll, ncol=36))
rownames(coll_random_ages) <- coll_dat$collection_number
init_dat_names <- c('coll_num', 'lat', 'lon', 'cell', 'centerlon', 'centerlat')
replicate_names <- c()
for (ind in 1:30) {
  name <- paste0('replicate', ind)
  replicate_names <- c(replicate_names, name)
}
column_names <- c(init_dat_names, replicate_names)
colnames(coll_random_ages) <- column_names


## Populate first 3 columns of dataframe with info from coll_dat
for (ind in 1:num_coll) {
  coll_random_ages[ind,1] <- coll_dat[ind, 1]
  coll_random_ages[ind,2] <- round(coll_dat[ind, 8], digits = 2)
  coll_random_ages[ind,3] <- round(coll_dat[ind, 9], digits = 2)
}

## Assign grid cells for each collection
coll_random_ages$cell <- dgGEO_to_SEQNUM(dggs,coll_random_ages$lon,coll_random_ages$lat)$seqnum

#Converting SEQNUM to GEO gives the center coordinates of the cells
cellcenters <- dgSEQNUM_to_GEO(dggs,coll_random_ages$cell)

## Assign center coordinates to collections
coll_random_ages$centerlon <- as.numeric(unlist(round(cellcenters[["lon_deg"]], 1)))
coll_random_ages$centerlat <- as.numeric(unlist(round(cellcenters[["lat_deg"]], 1)))


#### RANDOM AGES REPLICATES ####

## Run loop to create 30 samples of random ages for each collection
for (ind in 7:36) { ## 100 replicates of each collection
  for (coll in 1:num_coll) { ## Randomly sample age within age range of coll. for each replicate
    min_age <- as.numeric(coll_dat$min_ma[coll])
    max_age <- as.numeric(coll_dat$max_ma[coll])
    Age <- runif(n=1, min = min_age, max = max_age)
    if (is.na(Age) == TRUE) { ## Test whether or not there are any errors in calculating random ages
      print(coll, ind)
    }
    Age <- round(Age, digits = 0)
    coll_random_ages[coll,ind] <- Age
    print(paste0('age replicate ', ind, ' of collection ', coll))
  }
}

## Write CSV of age replicates datframe ##
write.csv(coll_random_ages, file = "RandomAge.csv", row.names = FALSE)


### RECONSTRUCT PALEOCOORDINATES FOR EACH CELL REPLICATE IN EACH COLLECTION


# load data

coll_dat <- read_xlsx('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/colls_added_March_2025.xlsx')
coll_random_ages <- read.csv('/Users/amandagardiner/Dropbox/Amanda´s\ Masters/DeepDive/RandomAge_colls_March_2025.csv')


coll_random_ages$centerlat <- round(coll_random_ages$centerlat, digits = 1)
coll_random_ages$centerlon <- round(coll_random_ages$centerlon, digits = 1)

num_coll <- length(coll_dat$collection_number)


## Load in Epoch
epochs <- data.frame(epoch = c('Lower Jurassic', 'Middle Jurassic', 'Upper Jurassic', 'Lower Cretaceous', 'Upper Cretaceous', 'Paleocene', 'Eocene', 'Oligocene', 'Miocene', 'Pliocene', 'Pleistocene', 'Holocene'), 
                     start = c(201.4, 174.7, 161.5, 145, 100.5, 66, 56, 33.9, 23.03, 5.333, 2.58, 0.0117), 
                     end = c(174.7, 161.5, 145, 100.5, 66, 56, 33.9, 23.03, 5.333, 2.58, 0.0117, 0), 
                     midpoint = c(0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
for (i in 1:length(epochs$epoch)) {
  age_vec <- c(epochs[i,2], epochs[i,3])
  mid <- median(age_vec)
  epochs[i,4] <- mid
}


# create column names object
init_dat_names <- c('coll_num', 'lat', 'lon', 'cell', 'centerlon', 'centerlat')
replicate_names <- c()
for (ind in 1:5) {
  name <- paste0('replicate', ind)
  replicate_names <- c(replicate_names, name)
}
column_names <- c(init_dat_names, replicate_names)


#### PALEOCOORDINATES RECONSTRUCTION ####
### distinct(age, Long_cent, lat_cent)

## Create dataframe to store all paleocoordinates replicates with random ages
#### MODIFIED 20250308 ####
coll_paleocoord_lon <- data.frame(matrix(data = NA, nrow=num_coll, ncol=36))
coll_paleocoord_lat <- data.frame(matrix(data = NA, nrow=num_coll, ncol=36)) ## Since we are dealing with fewer collections I'm running all 30 replicates at once
####
# coll_paleocoord_lon <- data.frame(matrix(data = NA, nrow=num_coll, ncol=11)) # 10 sets of 10 reps = ncol 16, total is ncol=106
rownames(coll_paleocoord_lon) <- coll_dat$collection_number
colnames(coll_paleocoord_lon) <- column_names
coll_paleocoord_lon$coll_num <- coll_dat$collection_number
#### MODIFIED 20250308 ####
coll_paleocoord_lon$lat <- coll_dat$latitude
coll_paleocoord_lon$lon <- coll_dat$longitude
#coll_paleocoord_lon$lat <- coll_dat$lat
#coll_paleocoord_lon$lon <- coll_dat$lon
####
coll_paleocoord_lon$cell <- coll_random_ages$cell
coll_paleocoord_lon$centerlon <- coll_random_ages$centerlon
coll_paleocoord_lon$centerlat <- coll_random_ages$centerlat

# coll_paleocoord_lat <- data.frame(matrix(data = NA, nrow=num_coll, ncol=11)) # 10 sets of 10 reps = ncol 16, total is ncol=106
rownames(coll_paleocoord_lat) <- coll_dat$collection_number
colnames(coll_paleocoord_lat) <- column_names
coll_paleocoord_lat$coll_num <- coll_dat$collection_number
#### MODIFIED 20250308 ####
coll_paleocoord_lat$lat <- coll_dat$latitude_r
coll_paleocoord_lat$lon <- coll_dat$longitude_r
#coll_paleocoord_lat$lat <- coll_dat$lat
#coll_paleocoord_lat$lon <- coll_dat$lon
####
coll_paleocoord_lat$cell <- coll_random_ages$cell
coll_paleocoord_lat$centerlon <- coll_random_ages$centerlon
coll_paleocoord_lat$centerlat <- coll_random_ages$centerlat


## Run coordinate reconstruction function 
dems <- fetch(dat="paleomap", var="dem")
demord <- matchtime(dems, epochs$midpoint)

#### MODIFIED 20250308 #### 
for (rep in 7:36) { 
  column <- rep
  for (ind in 1:num_coll) {
    tryCatch({
      replicate <- rep - 6
      x <- round(coll_random_ages[ind, 2], digits=1)
      y <- round(coll_random_ages[ind, 3], digits=1)
      paleo_lon_lat <- reconstruct(c(x,y), # c(5,6) == cell center coordinates
                                   age=coll_random_ages[ind,rep], 
                                   enumerate = FALSE, 
                                   model = 'MATTHEWS2016_mantle_ref')
      coll_paleocoord_lat[ind,column] <- paleo_lon_lat[1,2]
      coll_paleocoord_lon[ind,column] <- paleo_lon_lat[1,1]
      print(paste0('paleocoordinates replicate ', replicate, ' of collection ', ind))
    }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
  }
}
## NOTE: Lat and Lon labels are incorrectly swapped in coll_random_ages data table

print('saving paleocoordinates')
write.csv(coll_paleocoord_lat, file = './20250308_Added_FINSColl_paleolatitudes.csv', row.names = FALSE)
write.csv(coll_paleocoord_lon, file = './20250308_Added_FINSColl_paleolongitude.csv', row.names = FALSE)
print('finished saving paleocoordinates')

####
# chunks <- seq(1, num_coll, by = 5) # Chunks go up to 5926, will have to have separate loop for 5926 to 5929
# print('starting paleocoordinates reconstruction')
# 
# for (rep in 7:11) { # 7:106 total, 7:16 for 10 sets of 10 reps
#   column <- rep
#   for (ind in chunks) {
#     tryCatch({
#       replicate <- rep - 6
#       nextrow_two <- ind + 1
#       nextrow_three <- ind + 2
#       nextrow_four <- ind + 3
#       nextrow_five <- ind + 4
#       
#       if (ind == 5926) {
#         paleo_lon_lat <- reconstruct(coll_random_ages[ind:nextrow_four, c(3,2)], # c(5,6) == cell center coordinates
#                                      age=c(coll_random_ages[ind,rep], 
#                                            coll_random_ages[nextrow_two,rep], 
#                                            coll_random_ages[nextrow_three,rep], 
#                                            coll_random_ages[nextrow_four,rep] 
#                                      ), 
#                                      enumerate = FALSE, 
#                                      model = 'MATTHEWS2016_mantle_ref')
#         
#         coll_paleocoord_lat[ind,column] <- paleo_lon_lat[1,2]
#         coll_paleocoord_lon[ind,column] <- paleo_lon_lat[1,1]
#         
#         coll_paleocoord_lat[nextrow_two,column] <- paleo_lon_lat[2,2]
#         coll_paleocoord_lon[nextrow_two,column] <- paleo_lon_lat[2,1]
#         
#         coll_paleocoord_lat[nextrow_three,column] <- paleo_lon_lat[3,2]
#         coll_paleocoord_lon[nextrow_three,column] <- paleo_lon_lat[3,1]
#         
#         coll_paleocoord_lat[nextrow_four,column] <- paleo_lon_lat[4,2]
#         coll_paleocoord_lon[nextrow_four,column] <- paleo_lon_lat[4,1]
#         
#       }
#       else {
#         paleo_lon_lat <- reconstruct(coll_random_ages[ind:nextrow_five, c(3,2)], # c(5,6) == cell center coordinates
#                                      age=c(coll_random_ages[ind,rep], 
#                                            coll_random_ages[nextrow_two,rep], 
#                                            coll_random_ages[nextrow_three,rep], 
#                                            coll_random_ages[nextrow_four,rep], 
#                                            coll_random_ages[nextrow_five,rep]
#                                      ), 
#                                      enumerate = FALSE, 
#                                      model = 'MATTHEWS2016_mantle_ref')
#         
#         coll_paleocoord_lat[ind,column] <- paleo_lon_lat[1,2]
#         coll_paleocoord_lon[ind,column] <- paleo_lon_lat[1,1]
#         
#         coll_paleocoord_lat[nextrow_two,column] <- paleo_lon_lat[2,2]
#         coll_paleocoord_lon[nextrow_two,column] <- paleo_lon_lat[2,1]
#         
#         coll_paleocoord_lat[nextrow_three,column] <- paleo_lon_lat[3,2]
#         coll_paleocoord_lon[nextrow_three,column] <- paleo_lon_lat[3,1]
#         
#         coll_paleocoord_lat[nextrow_four,column] <- paleo_lon_lat[4,2]
#         coll_paleocoord_lon[nextrow_four,column] <- paleo_lon_lat[4,1]
#         
#         coll_paleocoord_lat[nextrow_five,column] <- paleo_lon_lat[5,2]
#         coll_paleocoord_lon[nextrow_five,column] <- paleo_lon_lat[5,1]
#         
#       }
#       print(paste0('paleocoordinates replicate ', replicate, ' of collection ', ind))
#     }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
#   }
# }
# 
# print('finished paleocoordinates with Matthew 2016 model')
# 
# for (rep in 8:8) { # 7:106 total
#   column <- rep
#   for (ind in 1:num_coll) {
#     tryCatch({
#       if (is.na(coll_paleocoord_lat[ind,rep]) == TRUE & is.na(coll_paleocoord_lon[ind,rep]) == TRUE) {
#         paleo_lon_lat <- reconstruct(coll_random_ages[ind, c(3,2)], 
#                                      age = coll_random_ages[ind,rep], 
#                                      enumerate = FALSE, 
#                                      model = 'PALEOMAP')
#         
#         coll_paleocoord_lat[ind,column] <- paleo_lon_lat[1,2]
#         coll_paleocoord_lon[ind,column] <- paleo_lon_lat[1,1]
#         
#         print(paste0('PALEOMAP replicate ', rep, ' of collection ', ind))
#       }
#     }, error=function(e){cat("ERROR :",conditionMessage(e), "\n")})
#   }
# }
# 
# print('finished paleocoordinates with PALEOMAP model')
# 
# 
# for (ind in 1:num_coll) {
#   if (is.na(coll_paleocoord_lat[ind,rep]) == TRUE & is.na(coll_paleocoord_lon[ind,rep]) == TRUE) {
#     print(paste0('row ', ind))
#     print(coll_paleocoord_lat[ind,])
#   }
# }
# 
# 
# ## Save paleocoordinates to csv
# print('saving paleocoordinates')
# write.csv(coll_paleocoord_lat, file = './17_02_23_FINSColl_paleolatitudes_V5_chunk2.csv', row.names = FALSE)
# write.csv(coll_paleocoord_lon, file = './17_02_23_FINSColl_paleolongitude_V5_chunk2.csv', row.names = FALSE)
# print('finished saving paleocoordinates')


#### ASSIGN OCEAN BASINS FROM THE PALEOLATITUDES AND LONGITUDES ####

## Create a dataframe to store the epochs
df_epoch <- data.frame(matrix(data = NA, nrow=num_coll, ncol=36))  # 7:106 total, 7:16 for 10 sets of 10 reps
rownames(df_epoch) <- coll_dat$collection_number
colnames(df_epoch) <- column_names
df_epoch$coll_num <- coll_dat$collection_number
df_epoch$lat <- coll_dat$latitude
df_epoch$lon <- coll_dat$longitude
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
df_ocean_basins$lat <- coll_dat$latitude
df_ocean_basins$lon <- coll_dat$longitude
df_ocean_basins$cell <- coll_random_ages$cell
df_ocean_basins$centerlon <- coll_random_ages$centerlon
df_ocean_basins$centerlat <- coll_random_ages$centerlat

df_30rep_lats <- read.csv('/Users/kristinakocakova/Dropbox/Analyses/Data/Other versions of Database/20250308_Added_FINSColl_paleolatitudes.csv')
df_30rep_lons <- read.csv('/Users/kristinakocakova/Dropbox/Analyses/Data/Other versions of Database/20250308_Added_FINSColl_paleolongitude.csv')

print('starting ocean basin assignment')
## Assign ocean basin based on paleocoord and age
for (rep in 7:30) {  # 7:106 total, 7:16 for 10 sets of 10 reps
  for (ind in 1:num_coll) {
    print(paste0('ocean basin replicate ', rep, ' of collection ', ind))
    if(is.na(df_30rep_lats[ind,rep]) && is.na(df_30rep_lons[ind,rep])) next
    #if (is.na(df_30rep_lats[ind,rep]) == FALSE && is.na(df_30rep_lons[ind,rep]) == FALSE) {
    if (df_epoch[ind,rep] == 'Lower Jurassic') {
      if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 120 && df_30rep_lats[ind,rep] > -40 && df_30rep_lats[ind,rep] < 45) {
        df_ocean_basins[ind,rep] <- 'Tethys'
      }
      else {
        df_ocean_basins[ind,rep] <- 'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Middle Jurassic') {
      if (df_30rep_lons[ind,rep] > 0 && df_30rep_lons[ind,rep] < 120 && df_30rep_lats[ind,rep] > -45 && df_30rep_lats[ind,rep] < 45) {
        df_ocean_basins[ind,rep] <- 'Tethys'
      }
      else {
        df_ocean_basins[ind,rep] <- 'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Upper Jurassic') {
      if (df_30rep_lons[ind,rep] > 22 && df_30rep_lons[ind,rep] < 130 && df_30rep_lats[ind,rep] < 30 && df_30rep_lats[ind,rep] > -40) {
        df_ocean_basins[ind,rep] <- 'Tethys'
      }
      else {
        df_ocean_basins[ind,rep] <-'Pacific'
      }
    }
    else if (df_epoch[ind,rep] == 'Lower Cretaceous') {
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

write.csv(df_paleoinfo, file = '/Users/kristinakocakova/Dropbox/Analyses/Data/Other versions of Database//22_02_23_FINSColl_Paleo_Coordinates_30rep_Modes.csv', row.names = FALSE)

