"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Quantify the contributors to PBDB
"""
import numpy as np
from pandas import *
from collections import Counter


fyle = read_csv("/Users/kristinakocakova/Downloads/pbdb_data(13).csv")

dyct = {}

for i, j in enumerate(fyle["collection_no"]):
    dyct[j] = []
    dyct[j].append(fyle["enterer"][i])

for i in dyct:
    l = len(dyct[i])
    if l > 1:
        print(i)

fyle_2 = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
sheet = read_excel(fyle_2, "Sheet2")

col_nos = sheet["collection_no_full"].to_list()

ent = []

for i in col_nos:
    if i not in dyct:
        ent.append("ADD")
    else:
        ent.append(dyct[i][0])

df = DataFrame()
df["col_no"] = col_nos
df["enterer"] = ent

df = df.dropna()

cols_missing_enterer = np.unique(df.loc[df["enterer"] == "ADD"]["col_no"])

#These following collections are now considered as duplicates in PBDB but were still valid when we downloaded data in 2020
dyct[214843] = ["Clapham M."]
dyct[214844] = ["Clapham M."]
dyct[214845] = ["Clapham M."]

Counter(df["enterer"])





colls = read_csv("/Users/kristinakocakova/Downloads/pbdb_data(13).csv")

dyct_2 = {}

for i, j in enumerate(colls["reference_no"]):
        dyct_2[j] = colls["collection_no"][i]


refs = read_csv("/Users/kristinakocakova/Downloads/pbdb_data(14).csv")

c = []

for i in refs["reference_no"]:
    if i in dyct_2:
        c.append(dyct_2[i])
    else:
        c.append("CHECK")

refs["collection_no"] = c


refs.to_csv("/Users/kristinakocakova/Downloads/pbdb_data(14)_col_nums.csv")