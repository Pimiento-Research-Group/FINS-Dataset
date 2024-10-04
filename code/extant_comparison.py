"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Comparison of species, genera, families and orders present in FINS to the list of extant taxa obtained from Stein et al. 2018
"""

from pandas import *

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