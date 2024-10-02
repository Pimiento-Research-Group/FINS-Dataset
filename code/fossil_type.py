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


#plot

#fossil type

collections = colls.dropna(subset= ["fossil_type"])

fos_type = []

for i in collections["fossil_type"].to_list():
    if ',' in i:
        x = i.split(', ')
        for j in x:
            fos_type.append(j)
    else:
        fos_type.append(i)

fos_type_clean = []

#remove whitespace at the beginning and end of strings
for i in fos_type:
    x = i.lstrip()
    y = x.rstrip()
    fos_type_clean.append(y)

count = Counter(fos_type_clean)

vals = list(count.values())
names = list(count.keys())
vals, names = zip(*sorted(zip(vals, names), reverse=True))

colors = [
'#ff6860',
'#ff7363',
'#ff7d68',
'#ff866c',
'#ff9071',
'#ff9877',
'#ffa17e',
'#ffa985',
'#ffb18c',
'#feb994',
'#fec19d',
'#fec8a6',
'#fed0af',
'#fed7b9'
]

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
fig, ax = plt.subplots()

plt.pie(vals, labels = names, labeldistance= 1.4, colors= colors, textprops={'fontsize': 7}, radius= 1, wedgeprops=dict(width=0.3, edgecolor='w'))
# labels= ranks,
ax.set(aspect="equal")
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')

centre_circle = plt.Circle((0, 0), 0.5, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show()












