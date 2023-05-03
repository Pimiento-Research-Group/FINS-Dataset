#Create an input file for PyRate program from an .xlsx file, options for species and genus level

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
        occurrences = occurrences[["accepted_name", "max_ma", "min_ma", "locality_id"]]

        #DROP DUPLICATES (Optional, occurrences of the same taxon from the same locality with identical ages could represent the same individual or population)
        occurrences = occurrences.drop_duplicates(keep="first")

        #WRITE OUTPUT FILE
        occurrences.to_csv(path_to_output, sep="\t", index=False)


pyrate_input("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/Database_Merged_V11_Final_new_ages.xlsx", "species", "/Users/kristinakocakova/Dropbox/test.csv")


