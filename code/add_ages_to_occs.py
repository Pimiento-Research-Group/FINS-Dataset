"""
Project: FINS Database
Author: Kristína Kocáková
Description:
Addition of time intervals and time in millions of years from Collections to the occurrences from respective Collections
"""

from pandas import *

fyle = ExcelFile("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/Database_Merged_V11_Final_new_ages.xlsx")
cols = read_excel(fyle, "Collections")
occs = read_excel(fyle, "Occurrences")

col_no_col = cols["collection_number"].to_list()
col_min_ma = cols["min_ma"].to_list()
col_max_ma = cols["max_ma"].to_list()
col_int_type = cols["time_interval_type"].to_list()
col_early_int = cols["early_interval"].to_list()
col_late_int = cols["late_interval"].to_list()

occ_no_col = occs["collection_no"].to_list()


min_ma = []
max_ma = []
int_type = []
early_int = []
late_int = []


for i in range(len(occ_no_col)):
    for j in range(len(col_no_col)):
        if occ_no_col[i] == col_no_col[j]:
            min_ma.append(col_min_ma[j])
            max_ma.append(col_max_ma[j])
            int_type.append(col_int_type[j])
            early_int.append(col_early_int[j])
            late_int.append(col_late_int[j])


occs2 = DataFrame(min_ma)
occs2["max_ma"] = max_ma
occs2["int_type"] = int_type
occs2["early_int"] = early_int
occs2["late_ist"] = late_int

occs2.to_excel("/Users/kristinakocakova/Dropbox/Analyses/Data/Master files/updated_min_max_times.xlsx")
# The output was then double-checked and copy-pasted into the Occurrences file

