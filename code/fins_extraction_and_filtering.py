"""
Project: Spatial ranges as a predictor of extinction through deep-time
Author: Kristína Kocáková
Description:
Extraction of data from FINS given the chosen parameters
"""

import os
from pandas import *
from collections import Counter

fins = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occurrences = read_excel(fins, "Occurrences")

# select only valid entries (considering both age and taxonomy)

occurrences = occurrences.loc[occurrences["age_evaluation"] == "valid"]
occurrences = occurrences.loc[occurrences["taxonomy_validation"] == "valid"]

# select only occurrences identified to a species or genus level

occurrences = occurrences.loc[(occurrences["rank"] == "species") | (occurrences["rank"] == "genus")]
occurrences = occurrences.loc[occurrences["early_interval"] != "present"]

# only occurrences with age resolution below 15 Myr
occurrences = occurrences.loc[occurrences["age_range"] <= 15]

# select columns - locality id (i.e. fossil site), species and genus name, paleocoordinates, minimum and maximum age, epoch (early_ and late_epoch columns are identical for occurrences with the selected age resolution)

occurrences = occurrences[["locality_id", "accepted_name", "genus", "rank", "max_ma", "min_ma", "early_epoch", "paleolat", "paleolon", "paleoocean"]]
occurrences = occurrences.rename(columns={"early_epoch": "epoch"})

# drop duplicates (Optional, occurrences of the same taxon from the same locality with identical ages could represent the same individual or population)
occurrences = occurrences.drop_duplicates(keep="first")

# extract only species
species = occurrences.loc[occurrences["rank"] == "species"]

# OPTIONAL: exclude singletons

counter = dict(Counter(species["accepted_name"]))

singletons = []
for i in counter:
    if counter[i] == 1:
        singletons.append(i)

species_no_sing = species[~species["accepted_name"].isin(singletons)]

# save files
cwd = os.getcwd()
occurrences.to_csv(cwd + "/data/species_genus_input.txt", sep = "\t", index = False)
species.to_csv(cwd + "/data/species_input.txt", sep = "\t", index = False)
species_no_sing.to_csv(cwd + "/data/species_input_no_sing.txt", sep = "\t", index = False)