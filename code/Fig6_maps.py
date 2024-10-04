"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Figure 5.
Plotting of distribution of occurrences through epochs and stages
"""

from pandas import *
import matplotlib.pyplot as plt
import geopandas as gpd
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.lines import Line2D
import seaborn as sns


from_pbdb = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
collections = read_excel(from_pbdb, "Collections")
occurrences = read_excel(from_pbdb, "Occurrences")

#Map A, bubble map of collections, color coded based on continent

x = 10

collections = collections[["latitude", "longitude", "continent", "n_occs"]]
no_occs_2 = np.array(collections["n_occs"])
no_occs_2 = no_occs_2/x # divide the actual number of occurrences by x, if left as is in raw data the bubbles are too big
collections["n_occs_2"] = no_occs_2

eur = collections.loc[collections["continent"] == "Europe"]
eur = sum(eur["n_occs"])

na = collections.loc[collections["continent"] == "North America"]
na = sum(na["n_occs"])

sa = collections.loc[collections["continent"] == "South America"]
sa = sum(sa["n_occs"])

asia = collections.loc[collections["continent"] == "Asia"]
asia = sum(asia["n_occs"])

afr = collections.loc[collections["continent"] == "Africa"]
afr = sum(afr["n_occs"])

oceania = collections.loc[collections["continent"] == "Oceania"]
oceania = sum(oceania["n_occs"])

antar = collections.loc[collections["continent"] == "Antarctica"]
antar = sum(antar["n_occs"])

oc = collections.loc[collections["continent"] == "Ocean"]
oc = sum(oc["n_occs"])


totals = {
    "continent": ["South America", "Antarctica", "Africa", "Ocean", "Europe", "Oceania", "Asia", "North America"],
    "lon": [-72.65, -56.665558, -9.6, -167, 15.064, 151.381, 70.918, -80.208], # coordinates for the large bubbles summarising the total number of occs in each continent
    "lat": [-6.866, -64.234718, 10.3, 24, 50.046, -33.005, 38.676, 36.7168],
    "n_occs": [sa/x, antar/x, afr/x, oc/x, eur/x, oceania/x, asia/x, na/x],
}

totals_df = DataFrame.from_dict(totals)

from palettable.cartocolors.qualitative import Prism_9

palette = {"Europe": Prism_9.mpl_colors[0], "Asia":Prism_9.mpl_colors[1], "North America": Prism_9.mpl_colors[2], "South America": Prism_9.mpl_colors[3], "Oceania":Prism_9.mpl_colors[4], "Ocean": Prism_9.mpl_colors[5], "Antarctica": Prism_9.mpl_colors[6], "Africa": Prism_9.mpl_colors[7] }

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42

#initiate plot
fig, ax = plt.subplots(figsize=(6.69291, 8.26772))

# plot world map
countries = gpd.read_file(
               gpd.datasets.get_path("naturalearth_lowres"))
countries.plot(color="#d7d7d7", ax = ax)

# plot collections
sns.scatterplot(data = collections, x="longitude", y="latitude", s = collections["n_occs_2"], alpha = 0.4, hue=collections["continent"], ax= ax, palette = palette)

# plot total continent values
sns.scatterplot(data = totals_df, x="lon", y="lat", s = totals_df["n_occs"], alpha = 0.3, ax= ax, hue = totals_df["continent"], palette= palette)

# remove righthand and top axis
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')

# axis labels
plt.xlabel("Longitude", fontsize = 7)
plt.ylabel("Latitude", fontsize = 7)
ax.tick_params(axis='both', which='major', labelsize=7)

# cutom legend
SA_patch = mpatches.Patch(color = Prism_9.mpl_colors[3], label = "South America")
Antar_patch = mpatches.Patch(color= Prism_9.mpl_colors[6], label = "Antarctica")
Afr_patch = mpatches.Patch(color = Prism_9.mpl_colors[7], label = "Africa")
Eur_patch = mpatches.Patch(color = Prism_9.mpl_colors[0], label = "Europe")
Oceania_patch = mpatches.Patch(color = Prism_9.mpl_colors[4], label = "Oceania")
Ais_patch = mpatches.Patch(color = Prism_9.mpl_colors[1], label = "Asia")
NOA_patch = mpatches.Patch(color = Prism_9.mpl_colors[2], label = "North America")
Ocean_patch = mpatches.Patch(color = Prism_9.mpl_colors[5], label = "Ocean")

plt.legend(handles = [Eur_patch, NOA_patch, SA_patch, Ais_patch, Afr_patch, Antar_patch,Oceania_patch, Ocean_patch], loc = "lower left", fontsize = 7, labelcolor = '#767676', framealpha = 0.4, edgecolor = "white")

plt.show()



#Map B, occurrences color coded based on origin (PBDB or literature)
occ_num = occurrences["occurrence_number"].to_list()
#
source = []

for i in occ_num:
    if "PBDB" in i:
        source.append("PBDB")
    elif "L" in i:
        source.append("FINS")

occurrences["Source"] = source

colors = {"PBDB": "#b56a9c", "FINS": "#037c6e"}

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
fig, ax = plt.subplots(figsize=(6.69291, 8.26772))

countries = gpd.read_file(
               gpd.datasets.get_path("naturalearth_lowres"))
countries.plot(color="#d7d7d7", ax = ax)

occurrences.plot(x="longitude", y="latitude", kind="scatter", c = occurrences["Source"].map(colors),
                 alpha = 0.1, ax = ax, s = 1, marker = "o")


plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')
plt.show()

# donut plots showing proportion of PBDB and Literature sourced occurrences

occurrences = occurrences.loc[occurrences["continent"] == "Asia"]
occ_num = occurrences["occurrence_number"].to_list()

l = 0
pbdb = 0
for i in occ_num:
    if "PBDB" in i:
        pbdb += 1
    elif "L" in i:
        l += 1


fig, ax = plt.subplots()

plt.pie([l, pbdb], labeldistance=1.4, colors=["#037c6e", "#b56a9c"], radius=1,
        wedgeprops=dict(width=0.3, edgecolor='w'))

centre_circle = plt.Circle((0, 0), 0.5, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show()









