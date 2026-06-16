"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Find taxa with uncertain nomenclature (containing aff., cf., ? or "")
Find how many of them only occur in the uncertainform - i.e. do we artificially inflate diversity by treating them as valid?
"""
import pandas as pd
import numpy as np

p = "/Volumes/External_memory/Dropbox/FINS_dataset/Data/Master_files/"

fins = pd.ExcelFile(p + "fins.xlsx")

occs = pd.read_excel(fins, "Occurrences")

# find species with uncertain nomenclature in the "raw" species name
uncert = occs[(occs["identified_name"].astype(str).str.contains("cf\.")) | (occs["identified_name"].astype(str).str.contains("aff\.")) | (occs["identified_name"].astype(str).str.contains("\?")) | (occs["identified_name"].astype(str).str.contains('"'))]

# exclude uncertain occurrences
norm = occs.drop(uncert.index)

# find unique valid names in both and compare

uncert_s = uncert.loc[uncert["rank"] == "species"]
uncert_g = uncert.loc[uncert["rank"] == "genus"]
uncert_f = uncert.loc[uncert["rank"] == "family"]
uncert_o = uncert.loc[uncert["rank"] == "order"]

missing_s = 0
missing_g = 0
missing_f = 0
missing_o = 0
missing = []

for i in np.unique(uncert_s["accepted_name"]):
    if i not in np.unique(norm["accepted_name"]):
        missing_s += 1
        missing.append(i)

for i in np.unique(uncert_g["genus"]):
    if i not in np.unique(norm["genus"]):
        missing_g += 1
        missing.append(i)

for i in np.unique(uncert_f["family"]):
    if i not in np.unique(norm["family"]):
        missing_f += 1
        missing.append(i)

for i in np.unique(uncert_o["order"]):
    if i not in np.unique(norm["order"]):
        missing_o += 1
        missing.append(i)


uniq_norm = np.unique(norm["accepted_name"])