"""
Project: FINS Database
Author: Kristína Kocáková
Description:
To enable users to collapse duplicates, "Unique" and "Duplicate" flags are added.
There are two ways of treating duplicates - using collection number and using locality ID, so two columns are created
"""

import numpy as np
import pandas as pd

p = "" # specify path to directory with FINS
occs = pd.read_csv(p + "Data_S3.csv")

fins = pd.ExcelFile('/Volumes/External_memory/Dropbox/FINS_dataset/Data/Master_files/fins_v2.xlsx')
occs = pd.read_excel(fins, "Occurrences")

invalid_occs = []

for i, row in occs.iterrows():
    if row["age_evaluation"] == "invalid" or row["age_evaluation"] == "unverifiable" or row["taxonomy_validation"] == "invalid":
        invalid_occs.append(row["occurrence_number"])

def flag_duplicates(df, invalid_occs, based_on=""):
    is_excluded = df["occurrence_number"].isin(set(invalid_occs))

    # Detect duplicates only among the non-excluded rows
    considered = df.loc[~is_excluded, ["accepted_name", based_on]]
    is_repeat = considered.duplicated(keep="first")

    # np.nan (not pd.NA) so the result renders in PyCharm's viewer
    flags = pd.Series(np.nan, index=df.index, dtype=object)
    flags.loc[~is_excluded] = is_repeat.map({False: "unique", True: "duplicate"})
    return flags.tolist()

occs["duplicates_collection_number"] = flag_duplicates(occs, invalid_occs= invalid_occs, based_on = "collection_no")
occs["duplicates_locality_id"] = flag_duplicates(occs, invalid_occs= invalid_occs, based_on = "locality_id")


