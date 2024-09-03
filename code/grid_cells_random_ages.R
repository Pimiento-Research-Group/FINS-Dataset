"""
Project: FINS Database
Author: Amanda Gardiner
Description:
Assignment of collections from FINS to grid cells, assignment of 30 random age replicates to each collection.
Save in a csv file.
"""

library(dplyr)
library(dggridR)
library(tidyr)
library(chronosphere)
library(readxl)

# Load in data
coll_dat <- read_xlsx('/Users/amandagardiner/Dropbox/Analyses/Data/Master\ files/fins.xlsx', 
                 sheet = 'Collections')

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

## Run loop to create 100 samples of random ages for each collection
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






























