import os
import pandas as pd
import numpy as np
from breakpoint import aggregate_all_operations
from blackscholes import get_total_opm
from allocation import aggregate_allocation_fvps
from test import opm_setter

df_cap = pd.read_excel('captable.xls')
df_asm = opm_setter(103075000.0)
thresholds, df_concat = aggregate_all_operations(df_cap)
optionprice, incremental_value_list, df_opm = get_total_opm(df_concat, df_asm)
df_concat = aggregate_allocation_fvps(
    df_concat, thresholds, incremental_value_list)
print(df_concat)
df_BPFT = df_concat.loc[:, ['BreakPoint From', 'BreakPoint To']]
df_opm.to_excel('option_allocation.xlsx')
df_BPFT.to_excel('BreakPointFromTo.xlsx')
df_FVPS = df_concat.loc[:, ['Security', 'Shares Outstanding', 'FVPS']]
df_FVPS.to_excel('FVPS.xlsx')
