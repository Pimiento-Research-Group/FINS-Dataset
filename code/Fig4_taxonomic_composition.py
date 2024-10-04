"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Figure 4.
Plotting of proportion of taxonomic ranks and taxonomic composition
"""

from pandas import *
import matplotlib.pyplot as plt
from collections import Counter

fyle = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occs = read_excel(fyle, "Occurrences")


#ranks
species = 0
genus = 0
family = 0
order = 0
other = 0

for i in occs["rank"]:
    if i == "species":
        species += 1
    elif i == "genus":
        genus += 1
    elif i == "family":
        family += 1
    elif i == "order":
        order += 1
    else:
        other += 1

counts = [species, genus, family, order, other]
colors = ["#037c6e", "#05998c", "#4fb9af", "#81cdc6", "#b3e0dc"]
ranks = ["Species", "Genus", "Family", "Order", "Other"]

plt.pie(counts, labels= ranks, labeldistance= 1.4, colors= colors, textprops={'fontsize': 9})
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')

plt.gca().spines['left'].set_color('#767676')
plt.gca().spines['bottom'].set_color('#767676')
plt.gca().tick_params(colors='#767676',)

centre_circle = plt.Circle((0, 0), 0.70, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show()

#taxonomic composition

batoids = 0
selachians = 0

for i in range(len(occs["accepted_name"])):
    if occs["superorder"][i] == "Batoidea":
        batoids += 1
    elif occs["superorder"][i] == "Galeomorphii" or occs["superorder"][i] == "Squalomorphii" or occs["genus"][i] == "Ptychodus" or occs["genus"][i] == "Odontorhytis" or occs["genus"][i] == "Cretomanta":
        selachians += 1

order_count = Counter(occs["order"])

counts = [batoids, selachians]
ranks = ["Batoids", "Selachians"]
colors = ["#0d403b", "#037c6e"]
order_counts = [order_count["Myliobatiformes"], order_count["Rajiformes"], order_count["Rhinopristiformes"], order_count["Torpediniformes"], order_count["Lamniformes"], order_count["Carcharhiniformes"], order_count["Orectolobiformes"], order_count["Hexanchiformes"], order_count["Squaliformes"], order_count["Squatiniformes"], order_count["Heterodontiformes"], order_count["Synechodontiformes"], order_count["Pristiophoriformes"], order_count["Echinorhiniformes"]]
order_colors = ["#fbc101", "#fed348", "#fedb68", "#fee8a1", "#b56a9c", "#d67cae", "#c674a4", "#eb92c0", "#cd7caa", "#ec9ac5", "#d484b0", "#eda2c9", "#da8bb5", "#eea9ce", "#53b8ac"]
order_labels = ["Myliobatiformes\n{i}".format(i = order_count["Myliobatiformes"]), "Rajiformes\n{i}".format(i = order_count["Rajiformes"]), "Rhinopristiformes\n{i}".format(i = order_count["Rhinopristiformes"]), "Torpediniformes\n{i}".format(i = order_count["Torpediniformes"]), "Lamniformes\n{i}".format(i = order_count["Lamniformes"]), "Carcharhiniformes\n{i}".format(i = order_count["Carcharhiniformes"]), "Orectolobiformes\n{i}".format(i = order_count["Orectolobiformes"]), "Hexanchiformes\n{i}".format(i = order_count["Hexanchiformes"]),"Squaliformes\n{i}".format(i = order_count["Squaliformes"]), "Squatiniformes\n{i}".format(i = order_count["Squatiniformes"]), "Heterodontiformes {i}".format(i = order_count["Heterodontiformes"]), "Synechodontiformes {i}".format(i = order_count["Synechodontiformes"]), "Pristiophoriformes {i}".format(i = order_count["Pristiophoriformes"]), "Echinorhiniformes {i}".format(i = order_count["Echinorhiniformes"])]

fig, ax = plt.subplots()

plt.pie(counts, labeldistance= 1.4, colors= colors, textprops={'fontsize': 12}, radius= 1, wedgeprops=dict(width=0.3, edgecolor='w'))
plt.pie(order_counts, colors= order_colors, radius= 0.7, wedgeprops=dict(width=0.3, edgecolor='w'), labeldistance= 1.1,textprops={'fontsize':8})
ax.set(aspect="equal")
plt.gca().spines['right'].set_color('none')
plt.gca().spines['top'].set_color('none')

centre_circle = plt.Circle((0, 0), 0.5, fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.show()
