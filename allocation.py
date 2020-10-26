import pandas as pd
import numpy as np

# get the allocation from all the base cases with no thresholds set


def get_base_allocation(df_cap):
    df_list_sum = []
    values = []
    allocation = []
    for i in range(len(pd.unique(df_cap['Seniority'])-1)):
        df_list_sum.append(df_cap[df_cap['Seniority'] == i+1].loc[:, 'LQ'])
    for i in range(len(df_list_sum)):
        series = df_list_sum[i]
        values.append(series[0:len(df_list_sum[i])])
    for i in range(len(values)):
        allocation.append(values[i]/values[i].sum())
    df_cap['Allocation'] = pd.concat(allocation)

# get the shares that must participat in allocation


def get_must_used_shares(df_cap):
    df_ma = pd.concat([df_cap[df_cap["Participating"] == True],
                       df_cap[df_cap.Security == "Common Shares"]])
    shares_must = df_ma['Shares Outstanding'].sum()
    return shares_must

# get a list of allocations and a list of threshold values


def get_threshold_value_allocation(df_cap, shares_must, thresholds):
    df_np = df_cap[df_cap["Participating"] == False]
    allocation = []
    threshold_values = []
    for threshold in thresholds:
        if df_np[df_np['Conversion_Threshold'] < threshold]['Shares Outstanding'].sum() > 0:
            allocation.append(df_np[df_np['Conversion_Threshold']
                                    < threshold]['Shares Outstanding'].sum()+shares_must)
            threshold_values.append(threshold)
        else:
            allocation.append(shares_must)
            threshold_values.append(0)
    return allocation, threshold_values

# get a data frame of the allocations for each threshold values


def get_allocation_df(df_cap, threshold_values, allocation):
    np_shares_alloc = {}
    alloc_dict = {}
    df_list = []
    df_ma = pd.concat([df_cap[df_cap["Participating"] == True],
                       df_cap[df_cap.Security == "Common Shares"]])
    df_np = df_cap[df_cap["Participating"] == False]
    for threshold_value in threshold_values:
        np_shares_alloc[threshold_value] = df_np[df_np['Conversion_Threshold']
                                                 < threshold_value]['Shares Outstanding'].values
    for threshold_value in threshold_values:
        tmp_list = np_shares_alloc[threshold_value]
        tmp2 = list(df_ma["Shares Outstanding"].values)
        for t in tmp_list:
            tmp2.append(t)
        alloc_dict[threshold_value] = tmp2
        tmp2 = None
    for i in range(len(allocation)):
        df_list.append(pd.DataFrame.from_dict(alloc_dict, orient='index').transpose(
        ).loc[:, threshold_values[i]]/allocation[i])
    df_alloc = pd.concat(df_list, axis=1)
    return df_alloc

# concat the base allocation to the cap table


def get_base_allocation_value(df_cap, incremental_value_list):
    df_allocation_lq = []
    concat_list = []
    for i in range(1, int(df_cap['Seniority'].max())+1):
        df_allocation_lq.append(
            df_cap[df_cap['Seniority'] == i]['Allocation']*incremental_value_list[i-1])
    for series in df_allocation_lq:
        concat_list.append(pd.DataFrame(series).dropna())
    df_base_allocation = pd.concat(concat_list)
    df_cap = pd.concat([df_cap, df_base_allocation], axis=1)
    return df_cap

# set the index of the threshold allocation


def df_allocation_index_setter(df_cap, df_alloc):
    df_ma = pd.concat([df_cap[df_cap["Participating"] == True],
                       df_cap[df_cap.Security == "Common Shares"]])
    df_np = df_cap[df_cap["Participating"] == False]
    df_alloc.index = df_ma.index.append(df_np[:-1].index)

# get the threshold allocation


def calculate_threshold_allocation(df_alloc, incremental_value_list, threshold_values):
    df_tmp_th = []
    tmp_inc = incremental_value_list[-len(threshold_values):]
    for i in range(len(tmp_inc)):
        df_tmp_th.append(tmp_inc[i]*df_alloc.iloc[:, i])
    df_tmp_alloc = pd.concat(df_tmp_th, axis=1)
    return df_tmp_alloc

# find the fair value per share


def calculate_fvps(df_tmp_alloc, df_cap, threshold_values):
    df_cap = pd.concat([df_cap, df_tmp_alloc], axis=1)
    df_cap = pd.concat(
        [df_cap, df_cap.iloc[:, -(len(threshold_values)+1):].sum(axis=1)], axis=1)
    df_cap['FVPS'] = df_cap.iloc[:, -1]/df_cap['Shares Outstanding']
    return df_cap

# aggregate previous operations


def aggregate_allocation_fvps(df_concat, thresholds, incremental_value_list):
    get_base_allocation(df_concat)
    shares_must = get_must_used_shares(df_concat)
    allocation, threshold_values = get_threshold_value_allocation(
        df_concat, shares_must, thresholds)
    df_alloc = get_allocation_df(df_concat, threshold_values, allocation)
    df_concat = get_base_allocation_value(df_concat, incremental_value_list)
    df_allocation_index_setter(df_concat, df_alloc)
    df_tmp_alloc = calculate_threshold_allocation(
        df_alloc, incremental_value_list, threshold_values)
    df_concat = calculate_fvps(df_tmp_alloc, df_concat, threshold_values)
    return df_concat
