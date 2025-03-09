import numpy as np
from pandas import *
from collections import Counter

fyle = read_csv("/Users/kristinakocakova/Downloads/pbdb_data(12).csv")

fyle_2 = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
sheet = read_excel(fyle_2, "Sheet2")

sheet = sheet.loc[sheet["identified_name"] == "None"]

fyle_filtered = fyle[['collection_no', 'identified_name', 'created', "ref_author", "ref_pubyr"]]

sheet_filtered = sheet[['collection_no_2', 'identified_name_2', 'created']]

fyle_filtered["combined"] = fyle_filtered["collection_no"].astype(str) + fyle_filtered["identified_name"]
sheet_filtered["collection_no_2"] = sheet_filtered["collection_no_2"].astype(int)
sheet_filtered["combined"] = sheet_filtered["collection_no_2"].astype(str) + sheet_filtered["identified_name_2"]

fyle_filtered["ref_pubyr"] = fyle_filtered["ref_pubyr"].astype(int)
fyle_filtered["reference"] = fyle_filtered["ref_author"] + " " + fyle_filtered["ref_pubyr"].astype(str)

col_no = []
ident_name = []
ref = []

for i, j in enumerate(fyle_filtered["combined"]):
    for k in sheet_filtered["combined"]:
        if j == k:
            col_no.append("PBDB_" + str(fyle_filtered["collection_no"].to_list()[i]))
            ident_name.append(fyle_filtered["identified_name"].to_list()[i])
            ref.append(fyle_filtered["reference"].to_list()[i])


df = DataFrame()
df["collection"] = col_no
df["identified_name"] = ident_name
df["reference"] = ref

df.to_csv("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/occs_added_March_2025.csv")