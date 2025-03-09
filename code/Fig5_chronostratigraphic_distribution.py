"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Figure 5.
Plotting of distribution of occurrences through epochs and stages
"""

from pandas import *
import matplotlib.pyplot as plt
import seaborn as sns

from_pbdb = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/fins.xlsx")
occs = read_excel(from_pbdb, "Occurrences")

epochs = [[145, 100.5], [100.5, 66], [66, 56], [56, 33.9], [33.9, 23.03], [23.03, 5.333], [5.333, 2.58], [2.58, 0.0117], [0.0117, 0]]

epochs_count = [0]*9

for index, row in occs.iterrows():
    for j, k in enumerate(epochs):
        if row["min_ma"] >= k[1] and row["max_ma"] <= k[0]:
            epochs_count[j] += 1

stages = [[145, 139.8], [139.8, 132.6], [132.6, 129.4], [129.4, 121.4], [121.4, 113], [113, 100.5], [100.5, 93.9], [93.9, 89.8], [89.8, 86.3], [86.3, 83.6], [83.6, 72.1], [72.1, 66], [66, 61.6], [61.6, 59.2], [59.2, 56], [56, 47.8], [47.8, 41.2], [41.2, 37.71], [37.71, 33.9], [33.9, 27.82], [27.82, 23.03], [23.03, 20.44], [20.44, 15.97], [15.97, 13.82], [13.82, 11.63], [11.63, 7.246], [7.246, 5.333], [5.333, 3.6], [3.6, 2.58], [2.58, 1.8], [1.8, 0.774],[0.774, 0.129], [0.129, 0.0117], [0.0117, 0.0082], [0.0082, 0.0042], [0.0042, 0]]
stages_count = [0]*36

for index, row in occs.iterrows():
    for j, k in enumerate(stages):
        if row["min_ma"] >= k[1] and row["max_ma"] <= k[0]:
            stages_count[j] += 1


epoch_chrono_names = ["Lower Cret.", "Upper Cret.", "Paleocene", "Eocene", "Oligocene", "Miocene", "Pliocene", "Pleistocene", "Holocene"]
epoch_vals = epochs_count
epoch_cols = ['#8fd07b', '#67a155', '#e17c0a', '#df943e', '#f9b86d', '#ecbd0f', '#efca42', '#efd46e', '#f2dd8b']

stages_chrono = ["Berriasian", "Valanginian", "Hauterivian", "Barremian", "Aptian", "Albian", "Cenomanian", "Turonian", "Coniacian", "Santonian", "Campanian", "Maastrichtian", "Danian", "Selandian", "Thanetian", "Ypresian", "Lutetian", "Bartonian", "Priabonian", "Rupelian", "Chattian", "Aquitanian", "Burdigalian", "Langhian", "Serravalian", "Tortonian", "Messinian", "Zanclean", "Piacenzian", "Gelasian", "Calabrian", "Chibanian", "Stage 4", "Greenlandian", "Northgrippian", "Megalayan"]
stages_cols = ["#8ed084", "#9ad58d", "#a7d996", "#b4de9f", "#c2e1aa", "#c1e2a8", "#cee7b1", "#b8da7a", "#c5df82", "#d2e38c", "#dfe895", "#eaec9e", "#f9f1a8", "#ffc482", "#ffc58b", "#ffb38b", "#ffbe98", "#ffc8a5", "#ffd2b3", "#ffdbae", "#ffe5bc", "#ffee65", "#ffef6e", "#fff078", "#fff181", "#fff28b", "#fff395", "#fff8c5", "#fffacf", "#ffecb3", "#fff2ba", "#fff2c7", "#fff2dd", "#feecdb", "#fdece3", "#fdedec"]
stages_vals = stages_count

plt.rcParams['font.family'] = 'Arial'
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['xtick.labelsize'] = 7
plt.rcParams['ytick.labelsize'] = 7
fig, ax = plt.subplots(2, 1, figsize=(6.69291, 4.13386))
sns.set_style("white")

ax[0].bar(epoch_chrono_names, epoch_vals, color = epoch_cols, width= 1.)
sns.despine()
ax[0].set_xlabel("Epoch", fontsize = 9)
ax[0].set_ylabel("Number of occurrences", fontsize =7)
plt.tight_layout()

ax[0].bar_label(ax[0].containers[0], labels=epoch_vals, padding = 0.5, color = "#767676", fontsize = 9)
plt.xticks(fontsize = 7)

ax[1].bar(stages_chrono, stages_vals, color = stages_cols, width= 1.)
sns.despine()
plt.xticks( rotation = 45, fontsize = 7, rotation_mode='anchor', ha = "right")
ax[1].bar_label(ax[1].containers[0], labels=stages_vals, padding = 0.5, color = "#767676", fontsize = 6)
ax[1].set_xlabel("Stage", fontsize = 9)
ax[1].set_ylabel("Number of occurrences", fontsize =7)
plt.tight_layout()

plt.show()