from pandas import *
import numpy as np
from collections import Counter

f = '/Volumes/External_memory/Dropbox/FINS_dataset/Data/Master_files/fins.xlsx'
fins = ExcelFile(f)
cols = read_excel(fins, "Collections")
occs = read_excel(fins, "Occurrences")
# refs_l = read_excel(fins, "References_Literature")
# refs_p = read_excel(fins, "References_PBDB")
refs = read_excel(fins, "References")

sp = occs.loc[occs["rank"] == "species"]
gen = occs.loc[occs["rank"] == "genus"]
fam = occs.loc[occs["rank"] == "family"]
ord = occs.loc[occs["rank"] == "order"]

#---------- abstract ----------#
# no of unique taxa per rank
print("unique species: ", (len(np.unique(sp["accepted_name"]))) - 1) # substracts 1 as "unverifiable" shouldn't count
print("unique genera: ", (len(np.unique(occs["genus"]))) - 1) # substracts 1 as "unknown genus" shouldn't count
print("unique families: ", (len(np.unique(occs["family"]))) - 43) # substracts 4 as "incert.fam", "unknown family" and "incert.saedis" shouldn't count
print("unique orders: ", (len(np.unique(occs["order"]))) -2) # substracts 1 as "unknown order" and "incertae sedis" shouldn't count

# proportion of species-level occs

print("proportion of species: ", (len(sp)/len(occs))*100)

#---------- intro ----------#
# no of languages
# langs = list(refs_l["language"].values)
# langs = langs + list(refs_p["language"].values)
print("number of languages: ", (len(np.unique(list(refs["language"].values))) - 2)) # "unknown" and nan excluded

# no of unique taxa per rank
print("unique species: ", (len(np.unique(sp["accepted_name"]))) - 1) # substracts 1 as "unverifiable" shouldn't count
print("unique genera: ", (len(np.unique(occs["genus"]))) - 1) # substracts 1 as "unknown genus" shouldn't count
print("unique families: ", (len(np.unique(occs["family"]))) - 4) # substracts 4 as "incert.fam", "incert.Family", "unknown family" and "incert.saedis" shouldn't count
print("unique orders: ", (len(np.unique(occs["order"]))) -2) # substracts 1 as "unknown order" and "incertae sedis" shouldn't count


#---------- data records ----------#
# proportion of collections by source
cols_l = cols[cols["collection_number"].str.contains("L")]
cols_p = cols[cols["collection_number"].str.contains("PBDB")]
print("collections from lit: ", len(cols_l), ", ", (len(cols_l)/len(cols))* 100)
print("collections from PBDB: ", len(cols_p), ", ", (len(cols_p)/len(cols))* 100)

# proportion of occs by source
occs_l = occs[occs["occurrence_number"].str.contains("L")]
occs_p = occs[occs["occurrence_number"].str.contains("PBDB")]
print("occurrences from lit: ", len(occs_l), ", ", (len(occs_l)/len(occs))* 100)
print("occurrences from PBDB: ", len(occs_p), ", ", (len(occs_p)/len(occs))* 100)

# proportion of fossil types
cols_l = cols_l.fillna('')
foss_type = cols_l["fossil_type"].to_list()

split_foss_type = []

for i in foss_type:
    if "," in i:
        x = i.split(", ")
        for j in x:
            split_foss_type.append(j)
    else:
        split_foss_type.append(i)

counter = Counter(split_foss_type)
for i in counter:
    print(i, " ", counter[i], " ", (counter[i]/len(cols_l))*100)

# age validity cols

print("cols with invalid age: ", len(cols.loc[(cols["age_evaluation"] == "invalid") | (cols["age_evaluation"] == "unverifiable")]),
      (len(cols.loc[(cols["age_evaluation"] == "invalid") | (cols["age_evaluation"] == "unverifiable")])/len(cols)*100))

# validity occs
print("overall invalid occs: ", len(occs.loc[(occs["age_evaluation"] == "invalid") | (occs["age_evaluation"] == "unverifiable") | (occs["taxonomy_validation"] == "invalid")]),
      " ", (len(occs.loc[(occs["age_evaluation"] == "invalid") | (occs["age_evaluation"] == "unverifiable") | (occs["taxonomy_validation"] == "invalid")])/len(occs))*100)
print("age invalid occs: ", len(occs.loc[(occs["age_evaluation"] == "invalid") | (occs["age_evaluation"] == "unverifiable") & (occs["taxonomy_validation"] == "valid")]),
      " ", (len(occs.loc[(occs["age_evaluation"] == "invalid") | (occs["age_evaluation"] == "unverifiable") & (occs["taxonomy_validation"] == "valid")])/len(occs.loc[(occs["age_evaluation"] == "invalid") | (occs["age_evaluation"] == "unverifiable") | (occs["taxonomy_validation"] == "invalid")])*100))
print("taxonomy invalid occs: ", len(occs.loc[(occs["age_evaluation"] == "valid") & (occs["taxonomy_validation"] == "invalid")]),
      " ", (len(occs.loc[(occs["age_evaluation"] == "valid") & (occs["taxonomy_validation"] == "invalid")])/len(occs.loc[(occs["age_evaluation"] == "invalid") | (occs["age_evaluation"] == "unverifiable") | (occs["taxonomy_validation"] == "invalid")])*100))
print("both invalid occs: ", len(occs.loc[(occs["age_evaluation"] == "invalid") & (occs["taxonomy_validation"] == "invalid")]),
      " ", (len(occs.loc[(occs["age_evaluation"] == "invalid") & (occs["taxonomy_validation"] == "invalid")])/len(occs.loc[(occs["age_evaluation"] == "invalid") | (occs["age_evaluation"] == "unverifiable") | (occs["taxonomy_validation"] == "invalid")])*100))

# proportion of occs with synonyms (only considering genera and species have potential synonyms)
sp_gen = occs.loc[(occs["rank"] == "species")|(occs["rank"] == "genus")]
synon = 0
for i, j in enumerate(sp_gen["modified_identified_name"].values):
    j = j.replace(" sp.", "")
    if j != sp_gen["accepted_name"].values[i]:
        synon += 1

print("synonym proportion: ", (synon/len(occs)*100))

# names not updated to valid names
inval_syn = occs.loc[(occs["accepted_name"] == "unverifiable") | (occs["accepted_name"] == "nomen nudum") | (occs["accepted_name"] == "nomen dubium")]

print("synonyms not updated to valid name: ", len(inval_syn), " ", 100 -(len(inval_syn)/synon)*100)
print("prop of synonyms update to valid name: ", 100 -(len(inval_syn)/synon)*100)

# breakdown of invalid names
print("unverifiable names: ", len(occs.loc[(occs["accepted_name"] == "unverifiable")]))
print("unverifiable names lit: ", len(occs_l.loc[(occs_l["accepted_name"] == "unverifiable")]))
print("unverifiable names PBDB: ", len(occs_p.loc[(occs_p["accepted_name"] == "unverifiable")]))
print("nomen nudum: ", len(occs.loc[(occs["accepted_name"] == "nomen nudum")]))
print("nomen dubium: ", len(occs.loc[(occs["accepted_name"] == "nomen dubium")]))

# taxonomic evidence

print("occs without evidence (lit): ", len(occs_l.loc[occs_l["evidence_validation"] == "no_evidence"]), " ", (len(occs_l.loc[occs_l["evidence_validation"] == "no_evidence"])/len(occs_l)*100))
print("occs without evidence (PBDB): ", len(occs_p.loc[occs_p["evidence_validation"] == "no_evidence"]), " ", (len(occs_p.loc[occs_p["evidence_validation"] == "no_evidence"])/len(occs_p)*100))
print("occs without evidence (total): ", len(occs.loc[occs["evidence_validation"] == "no_evidence"]), " ",(len(occs.loc[occs["evidence_validation"] == "no_evidence"])/len(occs)*100))

# uncertain nomenclature

uncert = occs[(occs["identified_name"].astype(str).str.contains("cf\.")) | (occs["identified_name"].astype(str).str.contains("aff\.")) | (occs["identified_name"].astype(str).str.contains("\?")) | (occs["identified_name"].astype(str).str.contains('"'))]

print("uncertain nomenclature (total): ", len(uncert), " ", (len(uncert)/len(occs)*100))
print("cf: ", len(occs[(occs["identified_name"].astype(str).str.contains("cf\."))]), " ", (len(occs[(occs["identified_name"].astype(str).str.contains("cf\."))])/len(uncert)*100))
print("aff: ", len(occs[(occs["identified_name"].astype(str).str.contains("aff\."))]), " ", (len(occs[(occs["identified_name"].astype(str).str.contains("aff\."))])/len(uncert)*100))
print("?: ", len(occs[(occs["identified_name"].astype(str).str.contains("\?"))]), " ", (len(occs[(occs["identified_name"].astype(str).str.contains("\?"))])/len(uncert)*100))
print("quotes: ", len(occs[(occs["identified_name"].astype(str).str.contains('"'))]), " ", (len(occs[(occs["identified_name"].astype(str).str.contains('"'))])/len(uncert)*100))


# publication types
# pubs = list(refs_l["pubtype"].values) + list(refs_p["pubtype"].values)

pub_types = Counter(list(refs["pubtype"]))
for i in pub_types:
    print(i, " ", pub_types[i], " ", (pub_types[i]/len(refs))*100)

# lit by source
Counter(refs["source"])

# languages
# langs = list(refs_l["language"].values)
# langs = langs + list(refs_p["language"].values)
print("number of languages: ", (len(np.unique(list(refs["language"].values))) - 2)) # "unknown" and nan excluded

lang_c = Counter(refs["language"])
for i in lang_c:
    print(i, " ", lang_c[i], " ", (lang_c[i]/len(refs["language"]))*100)

# taxonomy

print("total unique taxa: ", len(np.unique(occs["accepted_name"])) - 3) # not counting unverfiable, nomen nudum and nomen dubium
not_in_pbdb = 0
for i in np.unique(occs_l["accepted_name"].values):
    if i not in np.unique(occs_p["accepted_name"].values):
        not_in_pbdb += 1

print("not in PBDB: ", not_in_pbdb)
print("unique species: ", len(np.unique(sp["accepted_name"])) - 3) # not counting unverfiable, nomen nudum and nomen dubium
batoids = []
selachians = []

for i, j in enumerate(sp["accepted_name"]):
    if j != "nomen nudum" or j != "nomen dubium" or j != "unverifiable":
        if sp["superorder"].values[i] == "Batoidea":
            batoids.append(sp["accepted_name"].values[i])
        elif sp["superorder"].values[i] == "Galeomorphii" or sp["superorder"].values[i] == "Squalomorphii" or sp["genus"].values[i] == "Odontorhytis" or sp["genus"].values[i] == "Cretomanta":
            selachians.append(sp["accepted_name"].values[i])
print("unique species (selachi): ", len(np.unique(selachians)), " ", (len(np.unique(selachians))/(len(np.unique(sp["accepted_name"]))))*100)
print("unique species (batos): ", len(np.unique(batoids)), " ", (len(np.unique(batoids))/(len(np.unique(sp["accepted_name"]))))*100)

print("unique genera: ", len(np.unique(occs["genus"])) - 1) # not counting unknown genus
batoids = []
selachians = []

for i, j in enumerate(occs["genus"]):
    if j == "unknown genus":
        continue
    else:
        if occs["superorder"].values[i] == "Batoidea":
            batoids.append(occs["genus"].values[i])
        elif occs["superorder"].values[i] == "Galeomorphii" or occs["superorder"].values[i] == "Squalomorphii" or occs["genus"].values[i] == "Odontorhytis" or occs["genus"].values[i] == "Cretomanta":
            selachians.append(occs["genus"].values[i])
print("unique genera (selachi): ", len(np.unique(selachians)), " ", (len(np.unique(selachians))/(len(np.unique(occs["genus"]))))*100)
print("unique genera (batos): ", len(np.unique(batoids)), " ", (len(np.unique(batoids))/(len(np.unique(occs["genus"]))))*100)

print("unique families: ", len(np.unique(occs["family"])) - 3) # not counting incert.fam.,  unknown family, incerae sedis
batoids = []
selachians = []

for i, j in enumerate(occs["family"]):
    if j == "unknown family" or j == "incert.fam." or j == "incert.sedis":
        continue
    else:
        if occs["superorder"].values[i] == "Batoidea":
            batoids.append(occs["family"].values[i])
        elif occs["superorder"].values[i] == "Galeomorphii" or occs["superorder"].values[i] == "Squalomorphii" or occs["genus"].values[i] == "Odontorhytis" or occs["genus"].values[i] == "Cretomanta":
            selachians.append(occs["family"].values[i])
print("unique families (selachi): ", len(np.unique(selachians)), " ", (len(np.unique(selachians))/(len(np.unique(occs["family"]))-3))*100)
print("unique families (batos): ", len(np.unique(batoids)), " ", (len(np.unique(batoids))/(len(np.unique(occs["family"]))-3))*100)

print("unique orders: ", len(np.unique(occs["order"])) - 2) # not counting unknown genus
batoids = []
selachians = []

for i, j in enumerate(occs["order"]):
    if j == "unknown order" or j == "incertae sedis":
        continue
    else:
        if occs["superorder"].values[i] == "Batoidea":
            batoids.append(occs["order"].values[i])
        elif occs["superorder"].values[i] == "Galeomorphii" or occs["superorder"].values[i] == "Squalomorphii" or occs["genus"].values[i] == "Odontorhytis" or occs["genus"].values[i] == "Cretomanta":
            selachians.append(occs["order"].values[i])
print("unique orders (selachi): ", len(np.unique(selachians)), " ", (len(np.unique(selachians))/(len(np.unique(occs["order"]))-2))*100)
print("unique orders (batos): ", len(np.unique(batoids)), " ", (len(np.unique(batoids))/(len(np.unique(occs["order"]))-2))*100)

# most abundant

sp_count = dict(Counter(sp["accepted_name"]))
sp_most_abundant = sorted(sp_count, key=sp_count.get, reverse=True)

print("most abundant sp: ", sp_most_abundant[0], sp_count[sp_most_abundant[0]], (sp_count[sp_most_abundant[0]]/len(occs))*100)
print("2nd most abundant sp: ", sp_most_abundant[1], sp_count[sp_most_abundant[1]], (sp_count[sp_most_abundant[1]]/len(occs))*100)

# taxonomic rep
tax = dict(Counter(occs["rank"]))
print("species: ", tax["species"], " ", (tax["species"]/len(occs))*100)
print("genus: ", tax["genus"], " ", (tax["genus"]/len(occs))*100)

# superorders

batos = occs.loc[occs["superorder"] == "Batoidea"]
selachis = occs.loc[(occs["superorder"] == "Galeomorphii") | (occs["superorder"] == "Squalomorphii") | (occs["genus"] == "Odontorhytis") | (occs["genus"] == "Cretomanta")]

print("selachis: ", len(selachis), (len(selachis)/len(occs))*100)
print("batos: ", len(batos), (len(batos)/len(occs))*100)

# orders

ord_count = dict(Counter(occs["order"]))
ord_count_abund = sorted(ord_count, key=ord_count.get, reverse=True)

print("most abundant order: ",ord_count_abund[0] , ord_count[ord_count_abund[0]], (ord_count[ord_count_abund[0]]/len(occs))*100)
print("2nd most abundant order: ", ord_count_abund[1], ord_count[ord_count_abund[1]], (ord_count[ord_count_abund[1]]/len(occs))*100)
print("least abundant order: ", ord_count_abund[-1], ord_count[ord_count_abund[-1]], (ord_count[ord_count_abund[-1]]/len(occs))*100)
print("least abundant order: ", ord_count_abund[-2], ord_count[ord_count_abund[-2]], (ord_count[ord_count_abund[-2]]/len(occs))*100)

# chronostratigraphy

int_count = dict(Counter(occs["int_type"]))
int_count_abund = sorted(int_count, key=int_count.get, reverse=True)

print("most abundant interval type: ",int_count_abund[0] , int_count[int_count_abund[0]], (int_count[int_count_abund[0]]/len(occs))*100)
print("2nd most abundant interval type: ", int_count_abund[1], int_count[int_count_abund[1]], (int_count[int_count_abund[1]]/len(occs))*100)

print("mean age range: ", np.mean(occs["age_range"]))

epochs = ["Lower Cretaeous", "Upper Cretaceous", "Paleocene", "Eocene", "Oligocene", "Miocene", "Pliocene", "Pleistocene", "Holocene"]
epoch_temp = [[145, 100.5], [100.5, 66], [66, 56], [56, 33.9], [33.9, 23.03], [23.03, 5.333], [5.333, 2.58], [2.58, 0.0117], [0.0117, 0]]

epochs_count = dict()

for i in epochs:
    epochs_count[i] = 0

for index, row in occs.iterrows():
    for j, k in enumerate(epochs):
        if row["min_ma"] >= epoch_temp[j][1] and row["max_ma"] <= epoch_temp[j][0]:
            epochs_count[k] += 1

for i in epochs:
    print(i, " ", epochs_count[i], " ", (epochs_count[i]/len(occs))*100)

# geographic
continents = Counter(occs["continent"])
for i in continents:
    print(i, " ", continents[i], " ", (continents[i]/len(occs))*100)

north_countries = ["Japan", "Australia", "New Zealand", "South Korea", "Israel"]

north = cols.loc[(cols["continent"] == "Europe") | (cols["continent"] == "North America") | (cols["country"].isin(north_countries))]

print("global north: ", sum(north["n_occs"].values), (sum(north["n_occs"].values)/len(occs))*100)
print("south: ", (len(occs)- sum(north["n_occs"].values)), ((len(occs)- sum(north["n_occs"].values))/len(occs))*100)

for i in np.unique(occs["continent"].values):
    subset = occs.loc[occs["continent"] == i]
    pbdb = subset[subset["occurrence_number"].str.contains("PBDB")]
    print("proportion of PBDB occs in ", i, len(pbdb), (len(pbdb)/len(subset))*100)

# -------- patterns and gaps -----------

lamni_carcharhini = occs.loc[(occs["order"] == "Lamniformes") | (occs["order"] == "Carcharhiniformes")]

print("proportion of Lamni and Carcharhinifomes: ", len(lamni_carcharhini), (len(lamni_carcharhini)/len(occs))*100)



