"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Find taxa with uncertain nomenclature (containing aff., cf., ? or "")
Mark them as "uncertain" in the taxonomy_validation column
Find how many of species only occur in the uncertain form - i.e. do we artificially inflate diversity by treating them as valid?

Mark occurrences which are not in the SR lookup table as "unverifiable" in the taxonomy_validation column
"""
import pandas as pd
import numpy as np
from collections import Counter

p = "/Volumes/External_memory/Dropbox/FINS_dataset/Data/Master_files/"

fins = pd.ExcelFile(p + "fins.xlsx")

occs = pd.read_excel(fins, "Occurrences")

# find uncertain occs and mark them as such
quote_class = '["\'\u2018\u2019\u201c\u201d]'   # straight + curly, single + double

markers = [
    r"aff\.",          # affinity
    r"cfr?\.",         # cf. and the Italian variant cfr.
    r"\?",             # question mark
    r"ex\.?\s*gr\.",   # ex gr. / ex. gr. / Ex gr.
    r"\bgr\.",          # bare 'gr.', e.g. "Dasyatis gr. Centroura"
    quote_class,       # quotation marks around a name
]
pattern = "|".join(markers)

uncert = occs["identified_name"].str.contains(pattern, case=False, regex=True)
occs.loc[uncert, "taxonomy_validation"] = "uncertain"

Counter(occs["taxonomy_validation"])

# export into a temporary file and copy paste the taxonomy_validation column to the main FINS file
occs.to_csv(p + "occs_uncertain_tax.csv", index = False)

# Check what proportion of the dataset is taken up by the uncertain occs
# exclude uncertain occurrences
uncert = occs.loc[occs["identified_name"].str.contains(pattern, case=False, regex=True)]
norm = occs.drop(uncert.index)

# find unique valid names in both and compare

uncert_s = uncert.loc[uncert["rank"] == "species"]
uncert_g = uncert.loc[uncert["rank"] == "genus"]
uncert_f = uncert.loc[uncert["rank"] == "family"]
uncert_o = uncert.loc[uncert["rank"] == "order"]

missing_s = 0
missing_g = 0
missing_f = 0
missing_o = 0
missing = []

for i in np.unique(uncert_s["accepted_name"]):
    if i not in np.unique(norm["accepted_name"]):
        missing_s += 1
        missing.append(i)

for i in np.unique(uncert_g["genus"]):
    if i not in np.unique(norm["genus"]):
        missing_g += 1
        missing.append(i)

for i in np.unique(uncert_f["family"]):
    if i not in np.unique(norm["family"]):
        missing_f += 1
        missing.append(i)

for i in np.unique(uncert_o["order"]):
    if i not in np.unique(norm["order"]):
        missing_o += 1
        missing.append(i)


uniq_norm = np.unique(norm["accepted_name"])

# identify occurrences with identified names that are not in the SR lookup table
# use the modified_identified_name column as this one contains the taxonomy that does not contain any typos and based on which the accepted names are assigned











