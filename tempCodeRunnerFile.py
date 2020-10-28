if df_asm['Equity Value'] > list(df_BF.dropna())[-1]:
#     surplus = df_asm['Equity Value'] - list(df_BF.dropna())[-1]
#     df_concat = aggregate_allocation_fvps(
#         df_concat, thresholds, incremental_value_list)
#     df_concat['FVPS'] = df_concat['FVPS'].fillna(0)+surplus/df_concat
# else: