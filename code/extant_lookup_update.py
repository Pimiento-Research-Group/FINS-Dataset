import os
from pandas import *
from collections import Counter
import numpy as np

lookup_old = ExcelFile("/Users/kristinakocakova/Dropbox/FINS_dataset/Data/Master_files/lookup_tables/Lookup_Taxonomy.xlsx")
species_old = read_excel(lookup_old, "Species")

lookup_new = ExcelFile("/Users/kristinakocakova/Dropbox/FINS_dataset/Data/Master_files/lookup_tables/Lookup_Taxonomy_extant_LW.xlsx")
species_new = read_excel(lookup_new, "Species")

dyct_new_full = {}

for i, row in species_new.iterrows():
    dyct_new_full[row[0]] = list(row[1:])

dyct_new_full = {k: [elem for elem in v if elem is not np.nan] for k, v in dyct_new_full.items()} # remove nans


dyct_old_full = {}

for i, row in species_old.iterrows():
    dyct_old_full[row[0]] = list(row[1:])

dyct_old_full = {k: [elem for elem in v if elem is not np.nan] for k, v in dyct_old_full.items()} # remove nans


# find species which are treated as valid names in the original table but are synonyms in the new table
outdated = []

for i in species_old["Species"]:
    for j in dyct_new_full:
        if i in dyct_new_full[j]:
            outdated.append(i)

for i in species_new["Species"]:
    for j in dyct_old_full:
        if i in dyct_old_full[j]:
            outdated.append(i)

# create new rows for these species with the correct valid names and synonyms

df_new = DataFrame(columns = species_new.columns)

for i in outdated:
    for j, row in species_new.iterrows():
        if i in list(row):
            df_new = concat([df_new, DataFrame(row).T])

# some old valid names were considered unique but are now synonyms of the same valid name, therefore multiple duplicate rows could have been produced above
# drop duplicate rows

df_new = df_new.drop_duplicates(keep = "first")

# drop the rows of outdated species
species_old = species_old[~species_old["Species"].isin(outdated)]



#### FINS comparison to see how many species were not considered extant incorrectly

lookup_new = ExcelFile("/Users/kristinakocakova/Dropbox/FINS_dataset/Data/Master_files/lookup_tables/Other version of Lookup Table/Lookup_Taxonomy(extant)_05:05:2026.xlsx")
species_new = read_excel(lookup_new, "Species")
dyct_new_full = {}

for i, row in species_new.iterrows():
    dyct_new_full[row[0]] = list(row[1:])

dyct_new_full = {k: [elem for elem in v if elem is not np.nan] for k, v in dyct_new_full.items()} # remove nans

fins = ExcelFile("/Users/kristinakocakova/Dropbox/FINS_dataset/Data/Master_files/fins_v2.xlsx")
occs = read_excel(fins, "Occurrences")
outdated = []

for i in species_old["Species"]:
    for j in dyct_new_full:
        if i in dyct_new_full[j]:
            outdated.append(i)

c = 0
for i in np.unique(occs["accepted_name"]):
    if i in outdated:
        c += 1
        print(i)

