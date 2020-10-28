import pandas as pd
import numpy as np
from breakpoint import aggregate_all_operations
from opm import get_total_opm
from allocation import get_final_fvps
from test import opm_setter


# read the cap_table
df_cap = pd.read_excel('captable.xls')

# set the option pricing parameters
df_asm = opm_setter(equity_value=82925000.0)
print(df_asm)

# whole operations
thresholds, df_concat, df_BF = aggregate_all_operations(df_cap)
optionprice, incremental_value_list, df_opm = get_total_opm(df_concat, df_asm)
df_concat = get_final_fvps(df_concat, df_asm, df_BF,
                           thresholds, incremental_value_list)


# subsetting a dataframe that breakpoint from and break point to  coplumns
df_BPFT = df_concat.loc[:, ['BreakPoint From', 'BreakPoint To']]
# output the break point frome and breakpoint to into excel
df_BPFT.to_excel('BreakPointFromTo.xlsx')


# output the opm allocation into excel
df_opm.to_excel('option_allocation.xlsx')

# get a dataframe that stores Security Name, Shares Outstanding, and Fair Values per share
df_FVPS = df_concat.loc[:, ['Security', 'Shares Outstanding', 'FVPS']]
# output the result into excel
df_FVPS.to_excel('FVPS.xlsx')

# output the raw data file into excel
df_concat.to_excel('raw.xlsx')
