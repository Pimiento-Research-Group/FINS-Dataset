import os
from pandas import *
from collections import Counter
import numpy as np

fins = ExcelFile("/Volumes/External_memory/Dropbox/FINS_dataset/Data/Master_files/fins_v3.xlsx")
occs_f = read_excel(fins, "Occurrences")

occs_f = occs_f[occs_f["occurrence_number"].str.contains("PBDB_")]
occs_f = occs_f[occs_f["collection_no"].str.contains("PBDB_")]
occs_f["collection_no"] = occs_f["collection_no"].str.replace("PBDB_", "")
occs_f["collection_no"] = occs_f["collection_no"].astype("int")

occs_pbdb_orig = read_csv('/Volumes/External_memory/Dropbox/FINS_dataset/Data/Other versions of Database/occurrences.Chondrichthyes.orginaldownload.csv', header = 18)

occs_pbdb_cret = read_excel('/Volumes/External_memory/Dropbox/FINS_dataset/Data/Other versions of Database/occurrences_Cretaceous_download.xlsx')

occs_pbdb_merge = concat([occs_pbdb_orig, occs_pbdb_cret])

# see if there are any collections that are in FINS but not in the downloaded file
missing = []
for i in np.unique(occs_f["collection_no"]):
    if i not in np.unique(occs_pbdb_merge["collection_no"]):
        missing.append(i)

# load the file that has the occurrences from the missing collections and merge with the other
occs_pbdb_add = read_csv('/Volumes/External_memory/Downloads/pbdb_data(37).csv', header = 16)

occs_pbdb_merge = concat([occs_pbdb_merge, occs_pbdb_add])

occs_pbdb_merge = occs_pbdb_merge.drop_duplicates(subset = ["collection_no", "identified_name"])

occs_pbdb_merge.to_excel("/Volumes/External_memory/Downloads/pbdb_data_raw_original_plus_added_post_2021.xlsx", index = False)

## occs_pbdb_merge = read_excel("/Volumes/External_memory/Downloads/pbdb_data_raw.xlsx")

missing = []
for i in np.unique(occs_f["collection_no"]):
    if i not in np.unique(occs_pbdb_merge["collection_no"]):
        missing.append(i)

# still one col missing - 221132

# find matching identified names and collection numbers, extract occurrence number

for df in (occs_f, occs_pbdb_merge):
    df["identified_name"] = df["identified_name"].str.replace(r'\s+', '', regex=True).str.replace(r'"', '', regex=True).str.replace(r'<', '', regex=True).str.replace(r'>', '', regex=True).str.replace(r'\.', '', regex=True).str.lower()

matched = occs_f.merge(
    occs_pbdb_merge[["collection_no", "identified_name", "occurrence_no"]],
    on = ["collection_no", "identified_name"],
    how = "left", # keeps all rows, not just matched ones
)

matched["occurrence_no"] = matched["occurrence_no"].fillna("check")

# convert occ numbers to integers
occ_no = []
for i in matched["occurrence_no"]:
    if i != "check":
        occ_no.append(int(i))
    else:
        occ_no.append("check")

matched["occurrence_no"] = occ_no

matched.to_excel("/Volumes/External_memory/Dropbox/FINS_dataset/Data/Other versions of Database/corrercted_PBDB_occ_nos_June_2026.xlsx")


