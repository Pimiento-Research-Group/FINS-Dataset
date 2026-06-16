from pandas import *

f = '/Volumes/External_memory/Dropbox/FINS_dataset/Data/Master_files/fins.xlsx'
fins = ExcelFile(f)
cols = read_excel(fins, "Collections")
occs = read_excel(fins, "Occurrences")
# refs_l = read_excel(fins, "References_Literature")
# refs_p = read_excel(fins, "References_PBDB")
refs = read_excel(fins, "References")


col_refs = dict()

for i, j in enumerate(cols["reference_key"]):
    if j not in col_refs:
        col_refs[j] = []
        col_refs[j].append(cols["collection_number"].values[i])
    else:
        col_refs[j].append(cols["collection_number"].values[i])

occ_refs = dict()

for i, j in enumerate(occs["reference_key"]):
    if j not in occ_refs:
        occ_refs[j] = []
        occ_refs[j].append(occs["occurrence_number"].values[i])
    else:
        occ_refs[j].append(occs["occurrence_number"].values[i])


col_nums = []
occ_nums = []

for i in refs["reference_key"]:
    if i in col_refs:
        col_nums.append(", ".join(map(str, col_refs[i])))
    else:
        col_nums.append("NA")
    if i in occ_refs:
        occ_nums.append(", ".join(map(str, occ_refs[i])))
    else:
        occ_nums.append("NA")

refs["collection_number"] = col_nums
refs["occurrence_number"] = occ_nums

refs.to_csv("/Volumes/External_memory/Dropbox/FINS_dataset/Data/Other versions of Database/references_with_collection_and_occurrence_numbers_temp.txt", sep = "\t", index = False)

#the output was checked and manually copy-pasted to the FINS dataset (fins.xlsx)





