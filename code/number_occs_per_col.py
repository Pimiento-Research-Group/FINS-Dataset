"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Addition number of occurrences per collection to the Collections
"""

from pandas import *
from collections import Counter

database = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occurrences = read_excel(database, "Occurrences")
collections = read_excel(database, "Collections")

no_occ_dict = Counter(occurrences["collection_no"].to_list())

no_occs = []

for i, j in collections["collection_number"].to_list():
    no_occs.append(no_occ_dict[j])

collections["no_occs_new"] = no_occs

collections.to_excel("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins_new.xlsx")



