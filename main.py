import pandas as pd
import numpy as np
from breakpoint import aggregate_all_operations
from opm import get_total_opm
from allocation import aggregate_allocation_fvps
from test import opm_setter


# read the cap_table
df_cap = pd.read_excel('captable.xls')
# set the opm equity value, the other values will be near 0 by default
df_asm = opm_setter(103075000.0)
# get the thresholds and a dataframe that has all breakpoints
thresholds, df_concat = aggregate_all_operations(df_cap)
# get the opm allocation table, as well as incremental values and option prices
optionprice, incremental_value_list, df_opm = get_total_opm(df_concat, df_asm)
# returns a fataframe that also contains other operations
df_concat = aggregate_allocation_fvps(
    df_concat, thresholds, incremental_value_list)
print(df_concat)
# subsetting a dataframe that breakpoint from and break point to  coplumns
df_BPFT = df_concat.loc[:, ['BreakPoint From', 'BreakPoint To']]
# output the opm allocation into excel
df_opm.to_excel('option_allocation.xlsx')
# output the break point frome and breakpoint to into excel
df_BPFT.to_excel('BreakPointFromTo.xlsx')
# get a dataframe that stores Security Name, Shares Outstanding, and Fair Values per share
df_FVPS = df_concat.loc[:, ['Security', 'Shares Outstanding', 'FVPS']]
# output the result into excel
df_FVPS.to_excel('FVPS.xlsx')
