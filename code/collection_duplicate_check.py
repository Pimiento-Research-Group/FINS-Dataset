from pandas import *
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import connected_components

fins = ExcelFile("/Users/kristinakocakova/Dropbox/FINS_dataset/Data/Master_files/fins_v2.xlsx")
cols = read_excel(fins, "Collections")

# Max difference (in degrees) allowed between two rows on EACH coordinate.
max_diff = 0.2
coord_cols = ["latitude", "longitude"]

lat = cols["latitude"].to_numpy()
lon = cols["longitude"].to_numpy()
max_ma = cols["max_ma"].to_numpy()
min_ma = cols["min_ma"].to_numpy()

# Pairwise match: coordinates within max_diff AND both epochs identical.
within = np.abs(lat[:, None] - lat[None, :]) <= max_diff
within &= np.abs(lon[:, None] - lon[None, :]) <= max_diff
within &= max_ma[:, None] == max_ma[None, :]
within &= min_ma[:, None] == min_ma[None, :]

# Cluster mutually-similar rows into groups.
_, labels = connected_components(csr_matrix(within), directed=False)
cols["dup_group"] = labels

# Keep only groups with more than one member.
sizes = cols["dup_group"].value_counts()
dup_group_ids = sizes[sizes > 1].index
duplicates = cols[cols["dup_group"].isin(dup_group_ids)].copy()

# Sort so similar rows sit together.
duplicates = duplicates.sort_values("dup_group")
duplicates.to_excel("/Users/kristinakocakova/Dropbox/FINS_dataset/Data/Master_files/outlier_check/fins_collection_duplicates.xlsx", index=False)






