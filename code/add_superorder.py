"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Addition of the superorder taxonomic classification to occurrences based on their orders
"""


from pandas import *

galeomorphii = ["Heterodontiformes", "Orectolobiformes", "Lamniformes", "Carcharhiniformes"]

squalomorphii = ["Hexanchiformes", "Squaliformes", "Squatiniformes", "Synechodontiformes", "Pristiophoriformes", "Echinorhiniformes"]

batoidea = ["Myliobatiformes", "Rajiformes", "Rhinopristiformes", "Torpediniformes"]


from_pbdb = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occurences = read_excel(from_pbdb, "Occurrences")


superorder = []

for i in range(len(occurences["order"].to_list())):
    if occurences["order"].to_list()[i] in galeomorphii:
        superorder.append("Galeomorphii")
    elif occurences["order"].to_list()[i] in squalomorphii:
        superorder.append("Squalomorphii")
    elif occurences["order"].to_list()[i] in batoidea:
        superorder.append("Batoidea")
    elif occurences["order"].to_list()[i] == "incertae sedis":
        if occurences["genus"].to_list()[i] == "Belemnobatis":
            superorder.append("Batoidea")
        elif occurences["genus"].to_list()[i] == "Brachyrhizodus":
            superorder.append("Batoidea")
        elif occurences["genus"].to_list()[i] == "Cretomanta":
            superorder.append("incertae sedis")
        elif occurences["genus"].to_list()[i] == "Nanocetorhinus":
            superorder.append("incertae sedis")
        elif occurences["genus"].to_list()[i] == "Odontorhytis": #this one is recognised as a selachimorph when filtering data for selachimorph analyses
            superorder.append("incertae sedis")
        elif occurences["genus"].to_list()[i] == "Ptychodus": #this one is recognised as a selachimorph when filtering data for selachimorph analyses
            superorder.append("incertae sedis")
        elif occurences["genus"].to_list()[i] == "Spathobatis":
            superorder.append("Batoidea")
        else:
            superorder.append("CHECK")
    elif occurences["order"].to_list()[i] == "unknown order":
        if occurences["rank"].to_list()[i] == "clade" or occurences["rank"].to_list()[i] == "class" or occurences["rank"].to_list()[i] == "infraclass" or occurences["rank"].to_list()[i] == "subclass" or occurences["rank"].to_list()[i] == "subcohort":
            superorder.append("NA")
        elif occurences["rank"].to_list()[i] == "superorder":
            superorder.append(occurences["accepted_name"].to_list()[i])
        elif occurences["accepted_name"].to_list()[i] == "Batoidei":
            superorder.append("Batoidea")
        elif occurences["accepted_name"].to_list()[i] == "nomen nudum" or occurences["accepted_name"].to_list()[i] == "nomen dubium" or occurences["accepted_name"].to_list()[i] == "unverifiable":
            superorder.append("NA")
        elif occurences["accepted_name"].to_list()[i] == "Pseudoaetobatus" or occurences["accepted_name"].to_list()[i] == "Proteothrinax":
            superorder.append("NA")
        else:
            superorder.append("CHECK")

occurences["superorder"] = superorder

occurences.to_excel("/Users/kristinakocakova/Dropbox/superorder.xlsx")
# The output was then double-checked and copy-pasted into the Occurrences file
