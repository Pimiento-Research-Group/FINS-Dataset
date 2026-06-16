"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Updating of species and genera from synonyms to valid names based on their identified names, a table of synonyms from Shark-References is
required, see the data section of the FINS database GitHub page (https://github.com/Pimiento-Research-Group/FINS-Database/tree/main)
Save the dictionary of synonyms as a file
"""

from pandas import *
import numpy as np
import pickle

#1. Create a dictionary of species synonyms, assign accepted names to species
p = "/Volumes/External_memory/Dropbox/FINS_dataset/Data/Master_files/lookup_tables/Other version of Lookup Table/"

lookup_taxonomy_fos = ExcelFile(p + "Lookup_Taxonomy_version.30.3_Guinot.xlsx")
df = read_excel(lookup_taxonomy_fos, "Species")

# Initialize dictionary
synonym_dyct = {}

# Loop over each row
for _, row in df.iterrows():
    valid_name = row.iloc[0]  # first column = valid name

    # Map the valid name to itself
    synonym_dyct[valid_name] = valid_name

    # Remaining columns are synonyms
    synonyms = row.iloc[1:]

    # Add each synonym if not NaN
    for syn in synonyms:
        if notna(syn):
            synonym_dyct[syn] = valid_name

# save dictionary

with open(p + "synonym_dict.pkl", "wb") as fyle:
    pickle.dump(synonym_dyct, fyle)


#assign the accepted names

from_pbdb = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/Database_Merged_V11_Final.xlsx")
occurrences = read_excel(from_pbdb, "Occurrences")

identified_names = occurrences["modified_identified_name"].to_list()
identified_rank = occurrences["rank"].to_list()
accepted_names = occurrences["accepted_name"].to_list()


for i, j in enumerate(identified_rank):
    if j == "species":
        if identified_names[i] in synonym_dict:
            accepted_names[i] = synonym_dict[identified_names[i]]
        else:
            accepted_names[i] = "unidentified"


occurrences["accepted_name"] = accepted_names #exiting accepted names are now replaced with new accepted names in the occurrences dataframe

#2. Create a dictionary for genera synonyms and assign synonyms to species and genera

identified_genus = []

for i, j in enumerate(identified_rank):
    id_name = identified_names[i].split()
    ac_name = str(accepted_names[i]).split()
    if j == "genus":
        identified_genus.append(id_name[0])
    if j == "species":
        if accepted_names[i] == "unidentified":
            identified_genus.append(id_name[0])
        else:
            identified_genus.append(ac_name[0])
    elif j != "species" and j != "genus":
        identified_genus.append("unknown")

occurrences["identified_genus"] = identified_genus #new column in occurrences dataframe called "identified_genus"


# make a dictionary of genus synonyms

genus = read_excel(lookup_taxonomy_fos, "Genus")

genus_df = genus[["Genus", "Synonym.1", "Synonym.2", "Synonym.3", "Synonym.4", "Synonym.5"]]
genus_df_no_syn = genus_df[notnull(genus_df["Synonym.1"])] #drop all that have no synonyms

temp = genus_df_no_syn.set_index("Genus").T.to_dict("list") #converts a dataframe to dictionary using a specific column as index, i.e. keys
synonym_dict = {k: [elem for elem in v if elem is not np.nan] for k, v in temp.items()} #gets rid of nans in values

#add the valid names as value as well

genus_list = genus["Genus"].to_list()

for i in genus_list:
    if i in synonym_dict:
        if i not in synonym_dict[i]:
            synonym_dict[i].append(i)

#flip the dict, synonym = key, valid name = value

genus_syn_dict = {}

for i in synonym_dict:
    for j in synonym_dict[i]:
        genus_syn_dict[j] = i


#add genera with no synonyms

for i in genus_list:
    if i not in genus_syn_dict:
        genus_syn_dict[i] = i

accepted_genus = []

for i in identified_genus:
    if i in genus_syn_dict:
        accepted_genus.append(genus_syn_dict[i])
    else:
        accepted_genus.append("unknown genus")

occurrences["genus"] = accepted_genus #new collumn in dataframe occurences called "genus"
genus_occs = occurrences["genus"].to_list() #just re-naming the list

#add accepted name for occurences identified to genus level

for i, j in enumerate(identified_rank):
    if j == "genus":
        accepted_names[i] = genus_occs[i]

occurrences["accepted_name"] = accepted_names #overwrite old genera names to new accepted name

occurrences.to_excel("/Users/kristinakocakova/Dropbox/Sharks XT Dummy Files/fins_valid_names.xlsx")

# The output was then double-checked and copy-pasted into the Occurrences file
