"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Updating of species and genera from synonyms to valid names based on their identified names, a table of synonyms from Shark-References is
required, see the data section of the FINS database GitHub page (https://github.com/Pimiento-Research-Group/FINS-Database/tree/main)
"""

from pandas import *
import numpy as np

#1. Create a dictionary of species synonyms, assign accepted names to species

lookup_taxonomy_fos = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/Lookup_Taxonomy_version.30.3.xlsx")
species = read_excel(lookup_taxonomy_fos, "Species")

species_names = species["Species"].to_list()
first_syn = species["Synonym.1"] #not converted to list, needs to be dataframe for below to work

empty_syn1 = np.where(isnull(first_syn)) #rows with no synonyms

empty_syn1_indexes = []
for i in empty_syn1:
    for j in i:
        empty_syn1_indexes.append(j) #had to convert it into a list

no_syn_names = [] #species with no synonyms

for i in empty_syn1_indexes:
    j = species_names[i]
    no_syn_names.append(j)

#new dataframe with just species with synonyms
species_syn = species.drop(species.index[empty_syn1], axis=0, inplace=False)
speciess = species_syn["Species"].to_list() #list of species with synonyms

#dictionary of valid names (keys) and synonyms (values)
temp = species_syn.set_index("Species").T.to_dict("list") #converts a dataframe to dictionary using a specific column as index, i.e. keys
synonym_dict = {k: [elem for elem in v if elem is not np.nan] for k, v in temp.items()} #gets rid of nans in values


#this step needed to remove nans at the end of each value list, probably from the excel file
for i in synonym_dict:
    synonym_dict[i].remove(synonym_dict[i][-1])

#reversed synonym dict, synonym (key), valid name (value)
synonym_dict2 = {}

for i in synonym_dict:
    for j in synonym_dict[i]:
        synonym_dict2[j] = i

#add names with no synonyms, key and value the same
for i in no_syn_names:
    synonym_dict2[i] = i


#add names which have synonyms to also contain themselves, i.e. key and value the same
for i in speciess:
    synonym_dict2[i] = i

#assign the accepted names

from_pbdb = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/Database_Merged_V11_Final.xlsx")
occurrences = read_excel(from_pbdb, "Occurrences")

identified_names = occurrences["modified_identified_name"].to_list()
identified_rank = occurrences["rank"].to_list()
accepted_names = occurrences["accepted_name"].to_list()


for i, j in enumerate(identified_rank):
    if j == "species":
        if identified_names[i] in synonym_dict2:
            accepted_names[i] = synonym_dict2[identified_names[i]]
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
