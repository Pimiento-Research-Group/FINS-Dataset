"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Plotting of overview plots of the literature (languages, types of publications, publications per year, trends through time, etc.)
"""

from pandas import *
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import numpy as np
import palettable as pal

fyle = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
refs = read_excel(fyle, "References")

refs = refs.loc[refs["year"] >= 1970]

langs = Counter(refs["language"].to_list())

pub_types = Counter(refs["pubtype"].to_list())

refs = refs.astype({'year':'int'})

year = Counter(refs["year"].to_list())

dfu = refs[["year", "language"]]

dfu = dfu.groupby(["language", "year"]).size().reset_index(name="Freq")


sns.catplot(data=dfu, x="Year", y="Freq", hue="language", kind="swarm")

sns.catplot(data=refs, x="language", y="Year", kind = "violin", cut = 0)

plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.ylim(bottom = 1970)
plt.show()

#Donut plots
year = dict(sorted(year.items(), key=lambda x:x[1]))
year_labels = year.keys()
year_values = year.values()

langs = dict(sorted(langs.items(), key=lambda x:x[1], reverse= True))
langauge_labels = langs.keys()
language_values = langs.values()

pub_types = dict(sorted(pub_types.items(), key=lambda x:x[1], reverse= True))
pub_type_labels = pub_types.keys()
pub_type_values = pub_types.values()

from palettable.cmocean.sequential import Tempo_12_r

Acton = ['#2E214D', '#4A3A65', '#6A527E', '#8D628F', '#AB6694', '#BB6A98', '#CA739F', '#D381AA', '#D58DB2', '#D498BA', '#D3A4C2', '#D5AFCB', '#D7BDD4', '#DBCADD', '#E1D8E7', '#E6E6F0']
Tempo_12 = ['#1C495E', '#127576', '#419D82', '#6FAD8B', '#97BD9C', '#BDCEB5', '#DFE1D3', '#FFF6F4']

fig, ax = plt.subplots()

plt.pie(language_values, labeldistance= 1.4, textprops={'fontsize': 12}, radius= 1, wedgeprops=dict(width=0.3, edgecolor='w'), labels= langauge_labels, colors=Acton)
ax.set(aspect="equal")
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')

centre_circle = plt.Circle((0, 0), 0.5, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show()

#Pubs through Years

year_df = DataFrame(year.items(), columns=["Year", "Year_Count"])

sns.set_theme()
sns.lineplot(x = "Year",  y = "Year_Count", data = year_df, marker="o", color = "black", ci=None)
#hue = "language"
plt.gca().spines['left'].set_color('black')
plt.gca().spines['bottom'].set_color('black')
plt.xticks(np.arange(min(year_df["Year"].to_list()), max(year_df["Year"].to_list())+1, 5))
plt.yticks(np.arange(min(year_df["Year_Count"].to_list()), max(year_df["Year_Count"].to_list())+1, 1))
plt.xlabel("Year")
plt.ylabel("Number of Publications")
plt.show()


#Pubs through years and languages

singletons = ["Korean", "Swedish", "Ukranian", "Czech"]

sns.set_theme()
sns.lineplot(x = "Year",  y = "Freq", data = dfu, marker="o", color = "black", ci=None, hue = "language")
plt.gca().spines['left'].set_color('black')
plt.gca().spines['bottom'].set_color('black')
plt.xticks(np.arange(min(dfu["Year"].to_list()), max(dfu["Year"].to_list())+1, 5))
plt.yticks(np.arange(min(dfu["Freq"].to_list()), max(dfu["Freq"].to_list())+1, 1))
plt.show()

#use occs to assign countries

fins = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occurrences = read_excel(fins, "Occurrences")
collections = read_excel(fins, "Collections")

col_no = collections["collection_number"].to_list()
col_no_occs = occurrences["collection_no"].to_list()
col_country = collections["country"].to_list()

occ_country = []
for k in col_no_occs:
    for i, j in enumerate(col_country):
        if col_no[i] == k:
            occ_country.append(j)

occurrences["country"] = occ_country

occ_refs = occurrences["reference"].to_list()

#select the following three
occurrences = occurrences[["occurrence_number", "country", "reference"]]
occurrences = occurrences.drop_duplicates()
occurrences["occurrence_number"] = occurrences["occurrence_number"].str[:2]
occurrences = occurrences.drop_duplicates()
occurrences["year"] = occurrences["reference"].str[-4:]

occurrences['year'] = occurrences['year'].str.replace(' ','')

pg = occurrences.loc[occurrences["occurrence_number"] == "PG"]
pbdb = occurrences.loc[occurrences["occurrence_number"] == "PB"]




pbdb_year_counter = Counter(pbdb["year"].to_list())
pbdb_year = DataFrame(pbdb_year_counter.items(), columns=["Year", "Year_Count"])
pbdb_year = pbdb_year.sort_values(by= "Year")
pbdb_year = pbdb_year.astype({'Year':'int'})


year_df = DataFrame(year.items(), columns=["Year", "Year_Count"])


total = concat([year_df, pbdb_year])
total = total.astype({'Year':'int'})
total = total.sort_values(by= "Year")
total = total.groupby(by=total["Year"], as_index = False).sum()


sns.set_theme()
sns.lineplot(x = "Year",  y = "Year_Count", data = pbdb_year, marker="o", color = "#b56a9c", ci=None, label = "PBDB publications")
sns.lineplot(x = "Year",  y = "Year_Count", data = year_df, marker="o", color = "#037c6e", ci=None, label = "PG publication")
sns.lineplot(x = "Year",  y = "Year_Count", data = total, marker="o", color = "black", ci=None, label = "Total publications")
plt.gca().spines['left'].set_color('black')
plt.gca().spines['bottom'].set_color('black')
plt.xticks(np.arange(min(pbdb_year["Year"].to_list()), max(pbdb_year["Year"].to_list())+1, 10))
# plt.yticks(np.arange(min(year_df["Year_Count"].to_list()), max(year_df["Year_Count"].to_list())+1, 1))
plt.xlabel("Year")
plt.ylabel("Number of Publications")
plt.legend(loc = "upper left")
plt.show()

#Countries by year

countries_year = occurrences[["country", "year"]]
countries_year['year'] = countries_year['year'].str.replace('e','')

countries_year = countries_year.groupby(["country", "year"]).size().reset_index(name="Freq")

countries_year_2 = countries_year.sort_values(by = "year")
countries_year_2 = countries_year_2.astype({'year':'int'})

sns.set_theme()
sns.lineplot(x = "year",  y = "Freq", data = countries_year_2, marker="o", hue = "country", ci=None)
plt.gca().spines['left'].set_color('black')
plt.gca().spines['bottom'].set_color('black')
plt.xticks(np.arange(min(countries_year_2["year"].to_list()), max(countries_year_2["year"].to_list())+1, 10))
# plt.yticks(np.arange(min(year_df["Year_Count"].to_list()), max(year_df["Year_Count"].to_list())+1, 1))
plt.xlabel("Year")
plt.ylabel("Number of Publications")
plt.legend(loc = "upper left")
plt.show()

#by continent

fins = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occurrences = read_excel(fins, "Occurrences")
collections = read_excel(fins, "Collections")

occurrences = occurrences[["continent", "occurrence_number", "reference"]]

occurrences = occurrences.drop_duplicates()
occurrences["occurrence_number"] = occurrences["occurrence_number"].str[:2]
occurrences = occurrences.drop_duplicates()
occurrences["year"] = occurrences["reference"].str[-5:]

occurrences['year'] = occurrences['year'].str.replace(' ','')
occurrences['year'] = occurrences['year'].str.replace('a','')
occurrences['year'] = occurrences['year'].str.replace('b','')
occurrences['year'] = occurrences['year'].str.replace('c','')
occurrences['year'] = occurrences['year'].str.replace('d','')
occurrences['year'] = occurrences['year'].str.replace('e','')
occurrences['year'] = occurrences['year'].str.replace('n','')
occurrences['year'] = occurrences['year'].str.replace('l','')
occurrences['year'] = occurrences['year'].str.replace('z','')
occurrences['year'] = occurrences['year'].str.replace('.','')
occurrences['year'] = occurrences['year'].str.replace('1\(\)','2001')


continents = occurrences[["continent", "year"]]

continents = continents.groupby(["continent", "year"]).size().reset_index(name="Freq")

continents_2 = continents.sort_values(by = "year")
continents_2 = continents_2.astype({'year':'int'})

sns.set_theme()
palette ={"South America": "#1D6996", "Antarctica": "#5F4690", "Africa": "#EDAD08", "Europe": "#94346E", "Oceania": "#0F8554", "Asia": "#E17C05", "North America": "#CC503E","Ocean": "#38A6A5"}
sns.lineplot(x = "year",  y = "Freq", data = continents_2, marker="o", hue = "continent", ci=None, palette = palette)
plt.gca().spines['left'].set_color('black')
plt.gca().spines['bottom'].set_color('black')
plt.xticks(np.arange(min(continents_2["year"].to_list()), max(continents_2["year"].to_list())+1, 10))
# plt.yticks(np.arange(min(year_df["Year_Count"].to_list()), max(year_df["Year_Count"].to_list())+1, 1))
plt.xlabel("Year")
plt.ylabel("Number of Publications")
plt.legend(loc = "upper left", markerscale = 2)
plt.show()

df[['A', 'B']] = df['AB'].str.split(' ', 1, expand=True)
fyle = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occs = read_excel(fyle, "Occurrences")
occs = occs[["occurrence_number", "modified_identified_name", "accepted_name", "status", "rank", "order", "family"]]
occs["occurrence_number"] = occs["occurrence_number"].str[:2]
pg = occs.loc[occs["occurrence_number"] == "PG"]
pbdb = occs.loc[occs["occurrence_number"] == "PB"]

pbdb_count = Counter(pbdb["accepted_name"].to_list())
pg_count = Counter(pg["accepted_name"].to_list())

uniq_pbdb = unique(pbdb["accepted_name"].to_list())
uniq_lit = unique(pg["accepted_name"].to_list())
c = 0
for i in uniq_lit:
    if i not in uniq_pbdb:
        c += 1


c = 0
for i, j in enumerate(occs["modified_identified_name"]):
    if j != occs["accepted_name"][i]:
        c += 1

c = 0
for i, j in enumerate(pbdb["modified_identified_name"].to_list()):
    if j != pbdb["accepted_name"].to_list()[i]:
        c += 1

c = 0
for i, j in enumerate(pg["modified_identified_name"].to_list()):
    if j != pg["accepted_name"].to_list()[i]:
        c += 1

stein = read_excel("/Users/kristinakocakova/Dropbox/Kristina_PhD/Database/Extant_taxa_Stein_2018.xlsx")
stein = stein.loc[stein["Subclass"] != "Holocephali"]

stein_fam = unique(stein["Family"])
stein["Genus"] = stein['Scientific name'].str.split(' ').str[0]
stein_gen = unique(stein["Genus"])
stein_sp = unique(stein["Scientific name"])

fyle = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occs = read_excel(fyle, "Occurrences")
occs = occs[["occurrence_number", "modified_identified_name", "accepted_name", "status", "rank", "order", "family", "genus"]]

occs = occs.loc[occs["status"] == "extant"]

fins_fam = unique(occs["family"])
fins_gen = unique(occs["genus"])

for i in fins_fam:
    if i not in stein_fam:
        print(i)
for i in stein_fam:
    if i not in fins_fam:
        print(i)

c = 0
for i in stein_gen:
    if i not in fins_gen:
        c += 1

occs = occs.loc[occs["rank"] == "species"]
fins_sp = unique(occs["accepted_name"])

c = 0
for i in stein_sp:
    if i not in fins_sp:
        c += 1



fyle = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
cols = read_excel(fyle, "Collections")
cols = cols[["collection_number"]]
cols["collection_number"] = cols["collection_number"].str[:2]
pg = cols.loc[cols["collection_number"] == "PG"]
pbdb = cols.loc[cols["collection_number"] == "PB"]


counts = [2657, 3271,17103, 12931 ]
labels = ["PBDB Cols","PG Cols","PG Occs", "PBDB Occs"]
colors = ["#b381a2", "#218a7d","#037c6e","#b56a9c"]
fig, ax = plt.subplots()

plt.pie(counts, labeldistance= 1.4, colors= colors, textprops={'fontsize': 12}, radius= 1, wedgeprops=dict(width=0.3, edgecolor='w'))
# labels= ranks,
# plt.pie(order_counts, colors= order_colors, radius= 0.7, wedgeprops=dict(width=0.3, edgecolor='w'), labeldistance= 1.1,textprops={'fontsize':8})
#  labels=order_labels
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

lang_uniq = ['Spanish','German','French','Japanese','Russian' , 'Dutch', 'Portugese', 'Slovenian' ,'Italian' ,'Hungarian', 'Catalan', '']

cols = ["#f44336", "#e81e63", "#9c27b0", "#673ab7", "#3f51b5", "#2196f3", "#03a9f4", "#00bcd4", "#009688", "#4caf50", "#8bc34a", "#cddc39", "#ffeb3b", "#ffc107", "#ff9800", "#ff5722"]

Acton = ['#2E214D', '#4A3A65', '#6A527E', '#8D628F', '#AB6694', '#BB6A98', '#CA739F', '#D381AA', '#D58DB2', '#D498BA', '#D3A4C2', '#D5AFCB', '#D7BDD4', '#DBCADD', '#E1D8E7', '#E6E6F0']


fig, ax = plt.subplots(1, len(lang_uniq) + 1, sharey=True, sharex= True)
ax[0].spines['right'].set_visible(False)
ax[0].spines['top'].set_visible(False)
ax[0].tick_params(axis='both', colors="#505050", size = 12)
for i,j in enumerate(lang_uniq):
    ax[i + 1].spines['right'].set_visible(False)
    ax[i + 1].spines['top'].set_visible(False)
    ax[i + 1].set_xlabel(j, fontname = "Helvetica Neue", color = "#505050", fontsize = 12)
    ax[i + 1].set_xticks([10])
    ax[i + 1].barh(data = dfu.loc[dfu["language"] == j], y= "year", width = "Freq", color = Acton[i + 1])
    ax[i + 1].tick_params(axis='both', colors="#505050", size = 12)
ax[12].spines['right'].set_visible(False)
ax[12].spines['top'].set_visible(False)
ax[12].set_xlabel("")
ax[12].set_xticks([10])
ax[12].barh(data = dfu.loc[(dfu["language"] == "Czech") | (dfu["language"] == "Korean" )| (dfu["language"] == "Swedish") | (dfu["language"] == "Ukranian")] , y= "year", width = "Freq", color = Acton[12])

plt.show()

fig, ax = plt.subplots(1, len(lang_uniq) + 1, sharey=True, sharex= True)

ax[0].tick_params(axis='both', colors="#505050", size = 12)
ax[0].set_xlabel(j, fontname = "Helvetica Neue", color = "#505050", fontsize = 12)
ax[0].spines['right'].set_visible(False)
ax[0].spines['top'].set_visible(False)
ax[0].set_xlabel("English")
ax[0].set_xticks([25])
ax[0].barh(data=dfu.loc[dfu["language"] == "English"], y="year", width="Freq", color=Acton[0])
plt.show()










