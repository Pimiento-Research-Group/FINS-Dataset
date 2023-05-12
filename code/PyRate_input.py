"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Create an input file for PyRate program from an .xlsx file, options for species and genus level, options for additional filtering, e.g. by order, by age range, etc.
"""

"""
NOTE:

When filtering the data for Selachimorph taxa, please use the following
in order to include Ptychodus and Odontorhytis genera as Selachimorphs
despite having an incertae sedis superorder

selachis = ["Galeomorphii", "Squalomorphii"]
occurrences = occurrences.loc[(occurrences["superorder"].isin(selachis))| (occurrences["genus"] == "Ptychodus")| (occurrences["genus"] == "Odontorhytis")]

"""

from pandas import *


def pyrate_input(path_to_database, taxonomic_rank, path_to_output):
    database = ExcelFile(path_to_database)
    occurrences = read_excel(database, "Occurrences")

    # SELECT ONLY THE VALID ENTRIES (considering both age and taxonomy)

    occurrences = occurrences.loc[occurrences["evaluation_age"] == "valid_SHARKSXT_project"]
    occurrences = occurrences.loc[occurrences["taxonomy_validation"] == "valid_SHARKSXT_project"]

    #CREATE AN INPUT FILE FOR SPECIES
    if taxonomic_rank == "species":
        occurrences = occurrences.loc[occurrences["rank"] == "species"]

        #APPLY ANY ADDITIONAL FILTERS (Optional), e.g.:

        #Only occurrences with age resolution below 15 Myr
        occurrences = occurrences.loc[occurrences["age_range"] <= 15]
        #Only occurrences belonging to Lamniformes
        occurrences = occurrences.loc[occurrences["order"] == "Lamniformes"]

        #Select only required columns
        occurrences = occurrences[["accepted_name", "status", "max_ma", "min_ma", "locality_id"]]

        #DROP DUPLICATES (Optional, occurrences of the same taxon from the same locality with identical ages could represent the same individual or population)
        occurrences = occurrences.drop_duplicates(keep="first")

        #WRITE OUTPUT FILE
        occurrences.to_csv(path_to_output, sep="\t", index=False)

    #CREATE AN INPUT FILE FOR GENERA
    #INCLUDING OCCURRENCES IDENTIFIED DO A GENUS LEVEL AND THE GENUS OF OCCURRENCES IDENTIFIED TO A SPECIES LEVEL
    if taxonomic_rank == "genus":
        occurrences = occurrences.loc[(occurrences["rank"] == "species") | (occurrences["rank"] == "genus")]

        #APPLY ANY ADDITIONAL FILTERS (Optional), e.g.:

        #Only occurrences with age resolution below 15 Myr
        occurrences = occurrences.loc[occurrences["age_range"] <= 15]
        #Only occurrences belonging to Lamniformes
        occurrences = occurrences.loc[occurrences["order"] == "Lamniformes"]

        #Select only required columns
        occurrences = occurrences[["genus", "genus_status", "max_ma", "min_ma", "locality_id"]]

        #DROP DUPLICATES (Optional, occurrences of the same taxon from the same locality with identical ages could represent the same individual or population)
        occurrences = occurrences.drop_duplicates(keep="first")

        #WRITE OUTPUT FILE
        occurrences.to_csv(path_to_output, sep="\t", index=False)



pyrate_input("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx", "genus", "/Users/kristinakocakova/Dropbox/test.csv")



