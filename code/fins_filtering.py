
"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Script used for the filtering of the overall FINS dataset to produce datasets containing only data fitting our selected criteria
"""

"""
NOTE:

When filtering the data for Selachimorph taxa, please use the following
in order to include Cretomanta and Odontorhytis genera as Selachimorphs
despite having an incertae sedis superorder

selachis = ["Galeomorphii", "Squalomorphii"]
occurrences = occurrences.loc[(occurrences["superorder"].isin(selachis))| (occurrences["genus"] == "Odontorhytis")| (occurrences["genus"] == "Cretomanta")]

"""
from pandas import *

def pyrate_input(path_to_database, taxonomic_rank, path_to_output):
    database = ExcelFile(path_to_database)
    occurrences = read_excel(database, "Occurrences")

    # SELECT ONLY THE VALID ENTRIES (considering both age and taxonomy)

    occurrences = occurrences.loc[occurrences["evaluation_age"] == "valid_SHARKSXT_project"]
    occurrences = occurrences.loc[occurrences["taxonomy_validation"] == "valid_SHARKSXT_project"]
    occurrences = occurrences.loc[occurrences["early_interval"] != "present"]

    #CREATE AN INPUT FILE FOR SPECIES
    if taxonomic_rank == "species":
        occurrences = occurrences.loc[occurrences["rank"] == "species"]

        #APPLY ANY ADDITIONAL FILTERS (Optional), e.g.:

        #Only occurrences with age resolution below 15 Myr
        occurrences = occurrences.loc[occurrences["age_range"] <= 15]
        #Only occurrences belonging to Lamniformes
        # occurrences = occurrences.loc[occurrences["order"] == "Lamniformes"]
        # occurrences = occurrences.loc[(occurrences["paleolat"] >= -23.43632) & (occurrences["paleolat"] <= 23.43632)]

        #Remove occurrences of the same taxon, collection number and age range
        occurrences = occurrences.drop_duplicates(subset = ["collection_no", "accepted_name"], keep="first")
        #WRITE OUTPUT FILE
        occurrences.to_excel(path_to_output, index=False)

    #CREATE AN INPUT FILE FOR GENERA
    #INCLUDING OCCURRENCES IDENTIFIED DO A GENUS LEVEL AND THE GENUS OF OCCURRENCES IDENTIFIED TO A SPECIES LEVEL
    if taxonomic_rank == "genus":
        occurrences = occurrences.loc[(occurrences["rank"] == "species") | (occurrences["rank"] == "genus")]


        #APPLY ANY ADDITIONAL FILTERS (Optional), e.g.:

        #Only occurrences with age resolution below 15 Myr
        occurrences = occurrences.loc[occurrences["age_range"] <= 15]
        #Only occurrences belonging to Lamniformes
        # occurrences = occurrences.loc[occurrences["order"] == "Lamniformes"]

        #Remove occurrences of the same taxon, collection number and age range
        occurrences = occurrences.drop_duplicates(subset = ["collection_no", "genus"], keep="first")

        #WRITE OUTPUT FILE
        occurrences.to_excel(path_to_output, index=False)

pyrate_input("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx", "species", "/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/data_for_analyses/fins_filtered_species.xlsx")
