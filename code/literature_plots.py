"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Figure 3.
Plotting of overview plots of the literature (languages, types of publications, publications per year, trends through time, etc.)
"""

from pandas import *
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np
import re
import itertools

fyle = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
refs = read_excel(fyle, "References")
occurrences = read_excel(fyle, "Occurrences")

refs = refs.loc[refs["year"] >= 1970]

langs = Counter(refs["language"].to_list())

pub_types = Counter(refs["pubtype"].to_list())

refs = refs.astype({'year':'int'})

year = Counter(refs["year"].to_list())

#Donut plots

#Languages donut plot

langs = dict(sorted(langs.items(), key=lambda x:x[1], reverse= True))
langauge_labels = langs.keys()
language_values = langs.values()

Acton = ['#2E214D', '#4A3A65', '#6A527E', '#8D628F', '#AB6694', '#BB6A98', '#CA739F', '#D381AA', '#D58DB2', '#D498BA', '#D3A4C2', '#D5AFCB', '#D7BDD4', '#DBCADD', '#E1D8E7', '#E6E6F0']

fig, ax = plt.subplots()

plt.pie(language_values, labeldistance= 1.4, textprops={'fontsize': 12}, radius= 1, wedgeprops=dict(width=0.3, edgecolor='w'), labels= langauge_labels, colors=Acton)
ax.set(aspect="equal")
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')

centre_circle = plt.Circle((0, 0), 0.5, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show()

#Publication type donut plot

pub_types = dict(sorted(pub_types.items(), key=lambda x:x[1], reverse= True))
pub_type_labels = pub_types.keys()
pub_type_values = pub_types.values()

Tempo_12 = ['#1C495E', '#127576', '#419D82', '#6FAD8B', '#97BD9C', '#BDCEB5', '#DFE1D3', '#FFF6F4']

fig, ax = plt.subplots()

plt.pie(pub_type_values, labeldistance= 1.4, textprops={'fontsize': 12}, radius= 1, wedgeprops=dict(width=0.3, edgecolor='w'), labels= pub_type_labels, colors=Tempo_12)
ax.set(aspect="equal")
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')

centre_circle = plt.Circle((0, 0), 0.5, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show()

#Pubs through Years

#overall publications
occ_refs = occurrences["reference"].to_list()
occ_refs = unique(occ_refs)

year_total = []

for i in occ_refs:
    x = re.findall(r"\d+", i)
    year_total.append(x)

year_total = list(itertools.chain.from_iterable(year_total))

year_total_count = Counter(year_total)

df_total = DataFrame.from_dict({"year": year_total_count.keys(), "freq": list(year_total_count.values())})
df_total = df_total.astype({'year':'int'})

#separate pbdb and literature

lit = occurrences[occurrences["occurrence_number"].str.contains("L")]

lit_refs = lit["reference"].to_list()
lit_refs = unique(lit_refs)

year_lit = []

for i in lit_refs:
    x = re.findall(r"\d+", i)
    year_lit.append(x)

year_lit = list(itertools.chain.from_iterable(year_lit))

year_lit_count = Counter(year_lit)

df_lit = DataFrame.from_dict({"year": year_lit_count.keys(), "freq": list(year_lit_count.values())})
df_lit = df_lit.astype({'year':'int'})



pbdb = occurrences[occurrences["occurrence_number"].str.contains("PB")]

pbdb_refs = pbdb["reference"].to_list()
pbdb_refs = unique(pbdb_refs)

year_pb = []

for i in pbdb_refs:
    x = re.findall(r"\d+", i)
    year_pb.append(x)

year_pb = list(itertools.chain.from_iterable(year_pb))

year_pb_count = Counter(year_pb)

df_pb = DataFrame.from_dict({"year": year_pb_count.keys(), "freq": list(year_pb_count.values())})
df_pb = df_pb.astype({'year':'int'})


#full timeline plot
fig, ax = plt.subplots(
    figsize=(6.69291, 3))

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
sns.set_style("whitegrid")
sns.lineplot(x = "year",  y = "freq", data = df_pb, color = "#b56a9c", ci=None, label = "PBDB publications", ax = ax)
sns.lineplot(x = "year",  y = "freq", data = df_lit, color = "#037c6e", ci=None, label = "SR publication", ax=ax)
sns.lineplot(x = "year",  y = "freq", data = df_total, color = "black", ci=None, label = "Total publications", ax=ax)
plt.gca().spines['left'].set_color('black')
plt.gca().spines['bottom'].set_color('black')
plt.xticks(np.arange(min(df_pb["year"].to_list()), max(df_pb["year"].to_list())+1, 10))
# plt.yticks(np.arange(min(year_df["Year_Count"].to_list()), max(year_df["Year_Count"].to_list())+1, 1))
plt.xlabel("Year")
plt.ylabel("Number of Publications")
plt.legend(loc = "upper left")
plt.show()

# above 1970 plot

df_pb = df_pb.loc[df_pb["year"] >= 1970]
df_total = df_total.loc[df_total["year"] >= 1970]
df_lit = df_lit.loc[df_lit["year"] >= 1970]

fig, ax = plt.subplots(
    figsize=(6.69291, 3.6))

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
sns.set_style("whitegrid")
sns.lineplot(x = "year",  y = "freq", data = df_pb, marker="o", color = "#b56a9c", ci=None, label = "PBDB publications", ax = ax)
sns.lineplot(x = "year",  y = "freq", data = df_lit, marker="o", color = "#037c6e", ci=None, label = "SR publication", ax=ax)
sns.lineplot(x = "year",  y = "freq", data = df_total, marker="o", color = "black", ci=None, label = "Total publications", ax=ax)
plt.gca().spines['left'].set_color('black')
plt.gca().spines['bottom'].set_color('black')
plt.xticks(np.arange(min(df_pb["year"].to_list()), max(df_pb["year"].to_list())+1, 10))
# plt.yticks(np.arange(min(year_df["Year_Count"].to_list()), max(year_df["Year_Count"].to_list())+1, 1))
plt.xlabel("Year")
plt.ylabel("Number of Publications")
plt.legend(loc = "upper left")
plt.show()


# Frequency of languages through years

dfu = refs[["year", "language"]]

dfu = dfu.groupby(["language", "year"]).size().reset_index(name="Freq")

lang_uniq = ['Spanish','German','French','Japanese','Russian' , 'Dutch', 'Portugese', 'Slovenian' ,'Italian' ,'Hungarian', 'Catalan', '']

Acton = ['#2E214D', '#4A3A65', '#6A527E', '#8D628F', '#AB6694', '#BB6A98', '#CA739F', '#D381AA', '#D58DB2', '#D498BA', '#D3A4C2', '#D5AFCB', '#D7BDD4', '#DBCADD', '#E1D8E7', '#E6E6F0']

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
sns.set_style("white")
fig, ax = plt.subplots(1, len(lang_uniq) + 1, sharey=True, sharex= True, figsize=(6.69291, 4))
ax[0].spines['right'].set_visible(False)
ax[0].spines['top'].set_visible(False)
ax[0].tick_params(axis='both', colors="#505050", size = 12)
for i,j in enumerate(lang_uniq):
    ax[i + 1].spines['right'].set_visible(False)
    ax[i + 1].spines['top'].set_visible(False)
    ax[i + 1].set_xlabel(j, color = "#505050", fontsize = 12)
    ax[i + 1].set_xticks([10])
    ax[i + 1].barh(data = dfu.loc[dfu["language"] == j], y= "year", width = "Freq", color = Acton[i + 1])
    ax[i + 1].tick_params(axis='both', colors="#505050", size = 12)
ax[12].spines['right'].set_visible(False)
ax[12].spines['top'].set_visible(False)
ax[12].set_xlabel("")
ax[12].set_xticks([10])
ax[12].barh(data = dfu.loc[(dfu["language"] == "Czech") | (dfu["language"] == "Korean" )| (dfu["language"] == "Swedish") | (dfu["language"] == "Ukranian")] , y= "year", width = "Freq", color = Acton[12])

plt.show()

#english plotted separately, combined with above later
fig, ax = plt.subplots(1, len(lang_uniq) + 1, sharey=True, sharex= True, figsize=(6.69291, 4))
plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 1
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
sns.set_style("white")

ax[0].tick_params(axis='both', colors="#505050", size = 12)
ax[0].set_xlabel(j, fontname = "Helvetica Neue", color = "#505050", fontsize = 12)
ax[0].spines['right'].set_visible(False)
ax[0].spines['top'].set_visible(False)
ax[0].set_xlabel("English")
ax[0].set_xticks([25])
ax[0].barh(data=dfu.loc[dfu["language"] == "English"], y="year", width="Freq", color=Acton[0])
plt.show()










