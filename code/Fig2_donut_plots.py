"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Figure 2.
Plotting of PBDB and literature collections and occurrences, plotting of valid and invalid occurrences, plotting of fossil type
"""
from pandas import *
import matplotlib.pyplot as plt
from collections import Counter

#load data
fyle = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occs = read_excel(fyle, "Occurrences")
cols = read_excel(fyle, "Collections")

# Occurrences

pbdb_count = 0
lit_count = 0

for i in occs["occurrence_number"]:
    if "PB" in i:
        pbdb_count += 1
    elif "L" in i:
        lit_count += 1

counts = [pbdb_count, lit_count]
colors = ["#b56a9c","#037c6e"]

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
fig, ax = plt.subplots()

plt.pie(counts, labeldistance= 1.4, colors= colors, labels = ["PBDB", "Lit"], textprops={'fontsize': 12}, radius= 1, wedgeprops=dict(width=0.3, edgecolor='w'))
# labels= ranks,
ax.set(aspect="equal")
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')

centre_circle = plt.Circle((0, 0), 0.5, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show()

# Collections

pbdb_count = 0
lit_count = 0

for i in cols["collection_number"]:
    if "PB" in i:
        pbdb_count += 1
    elif "L" in i:
        lit_count += 1

counts = [pbdb_count, lit_count]
colors = ["#b56a9c","#037c6e"]

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
fig, ax = plt.subplots()

plt.pie(counts, labeldistance= 1.4, colors= colors, labels = ["PBDB", "Lit"], textprops={'fontsize': 12}, radius= 1, wedgeprops=dict(width=0.3, edgecolor='w'))
# labels= ranks,
ax.set(aspect="equal")
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')

centre_circle = plt.Circle((0, 0), 0.5, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show()

#fossil type

collections = cols.dropna(subset= ["fossil_type"])

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


# Age validity

valid = 0
invalid = 0

for i in occs["age_evaluation"]:
    if i == "valid":
        valid += 1
    else:
        invalid +=1 #this includes occs marked as unverifiable

counts = [valid, invalid]

colors = ["#00C3BB", "#018385"]

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
fig, ax = plt.subplots()

plt.pie(counts, labeldistance= 1.4, colors= colors, textprops={'fontsize': 12}, radius= 1, wedgeprops=dict(width=0.3, edgecolor='w'))
# labels= ranks,
ax.set(aspect="equal")
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')

# plt.gca().spines['left'].set_color('#767676')
# plt.gca().spines['bottom'].set_color('#767676')
# plt.gca().tick_params(colors='#767676',)

centre_circle = plt.Circle((0, 0), 0.5, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show()

# Nomenclature

valid = 0
invalid = 0

for i in occs["taxonomy_validation"]:
    if i == "valid":
        valid += 1
    else:
        invalid += 1

counts_validity = [valid, invalid]

colors_validity = ["#f598aa", "#ca7e9a"]

# valid names, synonyms, others
nomen = 0
unverifiable = 0

for i in occs["accepted_name"]:
    if i == "nomen nudum" or i == "nomen dubium":
        nomen += 1
    elif i == "unverifiable":
        unverifiable += 1

#find synonyms
modded_names = []

for i in range(len(occs["modified_identified_name"])):
    if occs["rank"][i] != "species":
        x = occs["modified_identified_name"][i].split()
        modded_names.append(x[0])
    else:
        modded_names.append(occs["modified_identified_name"][i])

valid_name = 0
synonym = 0

for i in range(len(occs["accepted_name"])):
    if occs["accepted_name"][i] != modded_names[i]:
        synonym += 1
    else:
        valid_name += 1

counts = [valid_name, synonym, unverifiable, nomen]
colors = ["#ff9ebb", "#ff7aa2", "#e05780", "#b9375e"]

#plot
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
fig, ax = plt.subplots()

plt.pie(counts, labels = ["valid", "synonym", "unverifiable", "nomen nudum/dubium"], labeldistance=1.4, colors=colors, textprops={'fontsize': 12}, radius=1,
        wedgeprops=dict(width=0.3, edgecolor='w'))
plt.pie(counts_validity, labeldistance=1.4, colors=colors_validity, textprops={'fontsize': 12}, radius=0.7,
        wedgeprops=dict(width=0.3, edgecolor='w'))
ax.set(aspect="equal")
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')

centre_circle = plt.Circle((0, 0), 0.5, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show()

# Taxonomic evidence

evidence = 0
no_evidence = 0

for i in occs["evidence_validation"]:
    if i == "with_evidence":
        evidence += 1
    else:
        no_evidence +=1

counts = [evidence, no_evidence]

colors = ["#FDD57E","#F7B940"]

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
fig, ax = plt.subplots()

plt.pie(counts, labeldistance= 1.4, labels= ["evidene", "no_evidence"], colors= colors, textprops={'fontsize': 12}, radius= 1, wedgeprops=dict(width=0.3, edgecolor='w'))
# labels= ranks,
ax.set(aspect="equal")
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')


centre_circle = plt.Circle((0, 0), 0.5, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show()













