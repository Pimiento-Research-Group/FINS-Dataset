"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Code used to generate a plot representing genus and species richness in each geological stage. The resulting plot is presented in the FINS Descriptor, Figure 5.
"""

from pandas import *
import matplotlib.pyplot as plt

from_pbdb = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occurrences = read_excel(from_pbdb, "Occurrences")

occurrences = occurrences.loc[occurrences["evaluation_age"] == "valid_SHARKSXT_project"]
occurrences = occurrences.loc[occurrences["taxonomy_validation"] != "invalid_SHARKSXT_project"]

occurrences = occurrences[["accepted_name", "early_interval", "rank", "genus"]]
occurrences_s = occurrences.loc[occurrences["rank"] == "species"]

stages = ["Berriasian", "Valanginian", "Hautverivian", "Barremian", "Aptian", "Albian", "Cenomanian", "Turonian", "Coniacian", "Santonian", "Campanian", "Maastrichtian", "Danian", "Selandian", "Thanetian", "Ypresian", "Lutetian", "Bartonian", "Priabonian", "Rupelian", "Chattian", "Aquitanian", "Burdigalian", "Langhian", "Serravalian", "Tortonian", "Messinian", "Zanclean", "Piacenzian", "Gelasian", "Calabrian", "Chibanian", "Stage 4", "Greenlandian", "Northgrippian", "Megalayan"]

dyct_s = {}

for i in stages:
    dyct_s[i] = []

for i, j in enumerate(occurrences_s["early_interval"].to_list()):
    if j in dyct_s:
        dyct_s[j].append(occurrences_s["accepted_name"].to_list()[i])

for i in dyct_s:
    dyct_s[i] = len(unique(dyct_s[i]))

print(dyct_s)
occurrences_g = occurrences.loc[(occurrences["rank"] == "species") | (occurrences["rank"] == "genus")]

stages = ["Berriasian", "Valanginian", "Hautverivian", "Barremian", "Aptian", "Albian", "Cenomanian", "Turonian", "Coniacian", "Santonian", "Campanian", "Maastrichtian", "Danian", "Selandian", "Thanetian", "Ypresian", "Lutetian", "Bartonian", "Priabonian", "Rupelian", "Chattian", "Aquitanian", "Burdigalian", "Langhian", "Serravalian", "Tortonian", "Messinian", "Zanclean", "Piacenzian", "Gelasian", "Calabrian", "Chibanian", "Stage 4", "Greenlandian", "Northgrippian", "Megalayan"]

dyct_g = {}

for i in stages:
    dyct_g[i] = []

for i, j in enumerate(occurrences_g["early_interval"].to_list()):
    if j in dyct_g:
        dyct_g[j].append(occurrences_g["genus"].to_list()[i])

for i in dyct_g:
    dyct_g[i] = len(unique(dyct_g[i]))

print(dyct_g)

plt.plot(dyct_s.keys(), dyct_s.values(), marker = "o", label = "species")
plt.plot(dyct_g.keys(), dyct_g.values(), marker = "o", c = "red", label = "genus")
plt.xticks(rotation = 45, ha = "right", fontsize = 12)
plt.ylabel("Number of unique taxa", fontsize = 12)
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.legend(edgecolor = "white")
plt.show()