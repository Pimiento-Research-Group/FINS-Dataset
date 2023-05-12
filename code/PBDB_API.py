import requests
from pandas import *

#DOWNLOAD THE DATA CONTAINING THE EVIDENCE

# pbdb = requests.get("https://paleobiodb.org/data1.2/occs/opinions.txt?base_name=Neoselachii&interval=Cretaceous,Cenozoic&show=basis")
# pbdb_data = pbdb.text
# with open("/Users/kristinakocakova/Dropbox/Kristina_PhD/Database/PBDB_taxonomic_validation.csv", "w") as f:
#     f.write(pbdb_data)

#MODIFY THE RESULTING FILE TO CONTAIN ONLY RELEVANT INFORMATION

pbdb = read_csv("/Users/kristinakocakova/Dropbox/Kristina_PhD/Database/PBDB_taxonomic_validation.csv")

pbdb = pbdb[["taxon_name", "basis", "author", "pubyr"]].copy()

#MERGE THE AUTHOR AND YEAR

ref = []
author = pbdb["author"].to_list()
year = pbdb["pubyr"].to_list()

for i, j in enumerate(author):
    x = j + " " + str(year[i])
    ref.append(x)

pbdb["ref"] = ref

