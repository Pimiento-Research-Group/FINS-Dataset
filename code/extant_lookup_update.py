import os

from PIL.ImageOps import expand
from pandas import *
from collections import Counter
import numpy as np

lookup_old = ExcelFile("/Users/kristinakocakova/Dropbox/FINS_dataset/Data/Master_files/lookup_tables/Lookup_Taxonomy.xlsx")
species_old = read_excel(lookup_old, "Species")

lookup_new = ExcelFile("/Users/kristinakocakova/Dropbox/FINS_dataset/Data/Master_files/lookup_tables/Lookup_Taxonomy_extant_LW.xlsx")
species_new = read_excel(lookup_new, "Species")

# rename all "Synonym.X" -> "Synonyms.X"
species_old = species_old.rename(
    columns=lambda c: c.replace("Synonym.", "Synonyms.") if c.startswith("Syn") else c
)

species_new = species_new.rename(
    columns=lambda c: c.replace("Synonym.", "Synonyms.") if c.startswith("Syn") else c
)

dyct_new_full = {}

for i, row in species_new.iterrows():
    dyct_new_full[row[0]] = list(row[1:])

dyct_new_full = {k: [elem for elem in v if elem is not np.nan] for k, v in dyct_new_full.items()} # remove nans


dyct_old_full = {}

for i, row in species_old.iterrows():
    dyct_old_full[row[0]] = list(row[1:])

dyct_old_full = {k: [elem for elem in v if elem is not np.nan] for k, v in dyct_old_full.items()} # remove nans


# find species which are treated as valid names in the original table but are synonyms in the new table
outdated = set()

# old valid name appears as a synonym in the new table
for name in species_old["Species"]:
    for syns in dyct_new_full.values():
        if name in syns:
            outdated.add(name)

# new valid name appears as a synonym in the old table
for name in species_new["Species"]:
    for syns in dyct_old_full.values():
        if name in syns:
            outdated.add(name)

# get replacement rows from the new file

# Collect rows where any cell (valid name or synonym) matches an outdated name
replacement_rows = []
for _, row in species_new.iterrows():
    row_values = {v for v in row if v is not np.nan}
    if row_values & outdated:               # non-empty intersection
        replacement_rows.append(row)

df_new = DataFrame(replacement_rows, columns=species_new.columns)

# drop columns absent from the old table
df_new = df_new.drop(columns=["Family", "Order", "Superorder"])

df_new = df_new.drop_duplicates(keep="first")

# drop outdated rows from old table and append replacements
species_old_updated = species_old[~species_old["Species"].isin(outdated)]
species_old_updated = concat([species_old_updated, df_new], ignore_index=True)

species_old_updated.to_excel("/Volumes/External_memory/Dropbox/FINS_dataset/Data/Master_files/lookup_tables/temp/Lookup_Taxonomy copy.xlsx", index = False)

extant = []

for i in species_old_updated["Species"]:
    if i in species_new["Species"].values:
        extant.append("extant")
    else:
        extant.append("extinct")

species_old_updated["status"] = extant


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

