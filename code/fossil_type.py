"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Add fossil type from occurrences to collections, calculate percentages, make plot of fossil types
"""

from pandas import *
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import Counter

fyle = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occs = read_excel(fyle, "Occurrences")
cols = read_excel(fyle, "Collections")

occs_fos_type = occs.dropna(subset= ["fossil_type"])
occs_fos_type = occs_fos_type.loc[occs_fos_type["fossil_type"] != "unspecified"]

# move fossil_type from occurrences to collections
occs = occs.fillna('')
dyct = {}

for i in occs["collection_no"]:
    if i not in dyct:
        dyct[i] = []

for index, row in occs.iterrows():
    if "," in row["fossil_type"]:
        x = row["fossil_type"].split(", ")
        for i in x:
            if i not in dyct[row["collection_no"]]:
                if i != "":
                    dyct[row["collection_no"]].append(i)
    else:
        if row["fossil_type"] not in dyct[row["collection_no"]]:
            if row["fossil_type"] != "":
                dyct[row["collection_no"]].append(row["fossil_type"])

fos_type = []
col_num = []

for index, row in cols.iterrows():
    fos_type.append(dyct[row["collection_number"]])
    col_num.append(row["collection_number"])

for i, j in enumerate(fos_type):
    fos_type[i] = ", ".join(j)

cols["fossil_type"] = fos_type

cols.to_excel("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/cols_temp.xlsx")


# count the number of types of fossils in collections

cols = cols.fillna('')
foss_type = cols["fossil_type"].to_list()

split_foss_type = []

for i in foss_type:
    if "," in i:
        x = i.split(", ")
        for j in x:
            split_foss_type.append(j)
    else:
        split_foss_type.append(i)

counter = Counter(split_foss_type)














