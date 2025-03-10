from pandas import *
from collections import Counter

cols = read_excel("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/colls_added_March_2025.xlsx")

# latitudinal band
lat_band = []

for i in cols["latitude"]:
    if i >= 23.436:
        lat_band.append("Northern Temperate")
    elif i < 23.436 and i > -23.436:
        lat_band.append("Tropical")
    elif i <= -23.436:
        lat_band.append("Southern Temperate")


cols["latitude_band"] = lat_band

# locality ID

cols["combined"] = cols["latitude"].astype(str) + cols["longitude"].astype(str) + cols["min_ma"].astype(str) + cols["max_ma"].astype(str)
dyct = {}

x = 5030

for i in cols["combined"]:
    if i not in dyct:
        dyct[i] = x
        x += 1

loc_ids = []

for i in cols["combined"]:
    loc_ids.append(dyct[i])

cols["locality_id"] = loc_ids

cols = cols.drop(["combined"], axis = 1)


cols.to_excel("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/colls_added_March_2025_updated.xlsx")


fins = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occs = read_excel(fins, "Occurrences")
cols = read_excel(fins, "Collections")

count = dict(Counter(occs["collection_no"]))

n_occs = []

for i in cols["collection_number"].to_list():
    n_occs.append(count[i])


cols["n_occs_new"] = n_occs

cols.to_excel("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins_new_n_occs.xlsx")


dyct_lat = {}
dyct_lon = {}
dyct_ocean = {}

for i, j in enumerate(cols["collection_number"]):
    dyct_lat[j] = cols["paleolatitude"].to_list()[i]
    dyct_lon[j] = cols["paleolongitude"].to_list()[i]
    dyct_ocean[j] = cols["paleoocean"].to_list()[i]

col_num = []
occ_lat = []
occ_lon = []
occ_oc = []

for i in occs["collection.1"]:
    col_num.append(i)
    occ_lat.append(dyct_lat[i])
    occ_lon.append(dyct_lon[i])
    occ_oc.append(dyct_ocean[i])

df = DataFrame()
df["col"] = col_num
df["paleolat"] = occ_lat
df["plaeolon"] = occ_lon
df["paleooc"] = occ_oc


df.to_excel("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/temp_occs.xlsx")


