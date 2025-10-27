"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Comparison of species, genera, families and orders present in FINS to the list of extant taxa obtained from Lookup_taxonomy(extant).xlsx
"""

from pandas import *

extant = ExcelFile("/Users/kristinakocakova/Dropbox/Kristina_PhD/Database/Lookup_taxonomy(extant).xlsx")
extant_sp = read_excel(extant, "Species")
extant_g = read_excel(extant, "Genus")
extant_f = read_excel(extant, "Family")

fyle = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occs = read_excel(fyle, "Occurrences")
occs = occs[["occurrence_number", "modified_identified_name", "accepted_name", "status", "rank", "order", "family", "genus"]]

occs = occs.loc[occs["status"] == "extant"]

fins_fam = unique(occs["family"])
fins_gen = unique(occs["genus"])

for i in fins_fam:
    if i not in extant_f:
        print(i)
for i in extant_f:
    if i not in fins_fam:
        print(i)

c = 0
for i in extant_g:
    if i not in fins_gen:
        c += 1

occs = occs.loc[occs["rank"] == "species"]
fins_sp = unique(occs["accepted_name"])

c = 0
for i in extant_sp:
    if i not in fins_sp:
        c += 1