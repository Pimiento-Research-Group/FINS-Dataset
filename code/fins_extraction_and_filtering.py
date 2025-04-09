"""
Project: Spatial ranges as a predictor of extinction through deep-time
Author: Kristína Kocáková
Description:
Extraction of data from FINS given the chosen parameters
"""
"""
NOTE:

When filtering the data for Selachimorph taxa, please use the following
in order to include Cretomanta and Odontorhytis genera as Selachimorphs
despite having an incertae sedis superorder

selachis = ["Galeomorphii", "Squalomorphii"]
occurrences = occurrences.loc[(occurrences["superorder"].isin(selachis))| (occurrences["genus"] == "Odontorhytis")| (occurrences["genus"] == "Cretomanta")]

"""

import os
from pandas import *
from collections import Counter

fins = ExcelFile("/Volumes/External_memory/Dropbox/FINS dataset/Data/Master files/fins.xlsx")
occurrences = read_excel(fins, "Occurrences")

# select only valid entries (considering both age and taxonomy)

occurrences = occurrences.loc[occurrences["age_evaluation"] == "valid"]
occurrences = occurrences.loc[occurrences["taxonomy_validation"] == "valid"]

# select only occurrences identified to a species or genus level

occurrences = occurrences.loc[occurrences["early_interval"] != "present"]

# only occurrences with age resolution below 15 Myr
occurrences = occurrences.loc[occurrences["age_range"] <= 15]

# drop duplicates (Optional, occurrences of the same taxon from the same locality with identical ages could represent the same individual or population)
occurrences = occurrences.drop_duplicates(subset=["collection_no", "accepted_name"], keep="first")

# OPTIONAL: Only occurrences belonging to a specific order
order = occurrences.loc[occurrences["order"] == "Squaliformes"]

# extract only species
species = order.loc[order["rank"] == "species"]

# OR extract genera
genera = occurrences.loc[(occurrences["rank"] == "species") | (occurrences["rank"] == "genus")]

# OPTIONAL: exclude singletons

counter = dict(Counter(species["accepted_name"]))

singletons = []
for i in counter:
    if counter[i] == 1:
        singletons.append(i)

species_no_sing = species[~species["accepted_name"].isin(singletons)]

# save files
species.to_excel("/Volumes/External_memory/Dropbox/FINS dataset/Data/Master files/data_for_analyses/orders_filtered/squaliformes.xlsx", index = False)

