"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Addition of taxonomy to occurrences based on their genus, a table of synonyms from Shark-References is
required, see the data section of the FINS database GitHub page (https://github.com/Pimiento-Research-Group/Sharks-XT-FINS-Database/tree/main)
"""


from pandas import *

lookup_taxonomy_fos = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/Lookup_Taxonomy_version.30.3.xlsx")
genus = lookup_taxonomy_fos["Genus"]

family = genus["Family"].to_list()
order = genus["Order"].to_list()

fins = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occurrences = read_excel(fins, "Occurrences")

rank = occurrences["rank"].to_list()
genus_occs = occurrences["genus"].to_list()
accepted_names = occurrences["accepted_name"].to_list()


fam_dict = {} #family - key, genera - value
genus_list = genus["Genus"].to_list()

for i, j in enumerate(family):
    if j not in fam_dict:
        fam_dict[j] = [genus_list[i]]
    else:
        fam_dict[j].append(genus_list[i])

#flip fam dict
fam_dict_2 = {}

for i in fam_dict:
    for j in fam_dict[i]:
        fam_dict_2[j] = i


order_dict = {} #order - key, genera - value

for i, j in enumerate(order):
    if j not in order_dict:
        order_dict[j] = [genus_list[i]]
    else:
        order_dict[j].append(genus_list[i])

#flip order dict

order_dict_2 = {}

for i in order_dict:
    for j in order_dict[i]:
        order_dict_2[j] = i


#family to order dictionary

fam_to_order_dict = {}

for i, j in enumerate(family):
    if j not in fam_to_order_dict:
        fam_to_order_dict[j] = order[i]

#add family and order columns to the file

family_list = []
order_list = []


for i, j in enumerate(rank):
    if j == "genus" or j == "species":
        if genus_occs[i] == "unknown genus":
            family_list.append("unknown family")
            order_list.append("unknown order")
        else:
            family_list.append(fam_dict_2[genus_occs[i]])
            order_list.append(order_dict_2[genus_occs[i]])
    elif j == "family":
        if accepted_names[i] == "Isuridae": #Isuridae are a junior synonym to Lamnidae
            family_list.append("Lamnidae")
            order_list.append("Lamniformes")
        elif accepted_names[i] == "Odontaspidae": #synonym
            family_list.append("Odontaspididae")
            order_list.append("Lamniformes")
        elif accepted_names[i] not in fam_to_order_dict:
            family_list.append("CHECK")
            order_list.append("CHECK")
        else:
            family_list.append(accepted_names[i])
            order_list.append(fam_to_order_dict[accepted_names[i]])
    elif j == "order":
        family_list.append("unknown family")
        order_list.append(accepted_names[i])
    else:
        family_list.append("unknown family")
        order_list.append("unknown order")

occurrences["order"] = order_list
occurrences["family"] = family_list


#check consistency between accepted name and family, if different change acc to family


for i, j in enumerate(accepted_names):
    if rank[i] == "family":
        if j != family_list[i]:
            if family_list[i] != "CHECK":
                accepted_names[i] = family_list[i]

occurrences["accepted_name"] = accepted_names



occurrences.to_excel("/Users/kristinakocakova/Dropbox/Sharks XT Dummy Files/fins_taxonomy.xlsx")

# The output was then double-checked and copy-pasted into the Occurrences file



















