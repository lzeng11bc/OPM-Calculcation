import numpy as np
import pandas as pd

# calcuate the liquadtion preference and conversion threshold
# Derive the breakpoints from the calculation. return the result
# in a dataframe


def calculate_break_point(df_cap):
    df_cap['LQ'] = pd.DataFrame(
        df_cap['Issue Price']*df_cap['Liquidation Preference']*df_cap['Shares Outstanding'])
    df_cap['BreakPoint From'] = df_cap['LQ'].groupby(
        df_cap['Seniority']).sum().cumsum()
    a = df_cap['BreakPoint From']
    a.index = range(len(a))
    df_cap['BreakPoint To'] = a
    df_BPFT = df_cap.iloc[:, -2:]
    df_cap["Conversion_Threshold"] = df_cap['LQ'] / \
        (df_cap["Shares Outstanding"]*df_cap['Conversion Rate'])
    return df_BPFT

# make a sorted list of all threshold values, and return the list.


def get_sorted_threshold_lists(df_cap):
    if(len(df_cap['Participating'] == False) != 0):
        thresholds = list(df_cap[df_cap['Participating'] ==
                                 False].Conversion_Threshold.sort_values())
    else:
        thresholds = []
    return thresholds

# get the positions of the participating shares, return the result in a dataframe


def get_participating_position(df_cap, thresholds):
    part_lq = []
    if len(df_cap['Participating'] == True) != 0:
        part_tmp = df_cap[df_cap['Participating'] == True]
        for threshold in thresholds:
            part_lq.append((part_tmp['Shares Outstanding']
                            * threshold+part_tmp['LQ']).sum())
        part_pos = pd.DataFrame(part_lq, index=thresholds)
    else:
        part_pos = pd.DataFrame()
    return part_pos

# get the positions of the non-participating shares, return the result in a dataframe


def get_non_participating_position(df_cap, thresholds):
    npart_lq = []
    if (len(df_cap['Participating'] == False) != 0):
        df_np_sort = df_cap[df_cap['Participating'] ==
                            False].sort_values("Conversion_Threshold")
    else:
        pass
    if len(thresholds) != 0:
        for threshold in thresholds:
            df_tmp_ls = df_np_sort[df_np_sort['Conversion_Threshold'] < threshold]
            df_tmp_gt = df_np_sort[df_np_sort['Conversion_Threshold'] >= threshold]
            lq_sum = np.sum(df_tmp_ls['Shares Outstanding']
                            * threshold*df_tmp_ls["Conversion Rate"])
            lq_sum += df_tmp_gt['LQ'].sum()
            npart_lq.append(lq_sum)
        npart_pos = pd.DataFrame(npart_lq, index=thresholds)
    else:
        npart_pos = pd.DataFrame()
    return npart_pos

# get the positions of the common shares, return the result in a dataframe


def get_common_share_position(df_cap, thresholds):
    cs = []
    if len(thresholds) != 0:
        for threshold in thresholds:
            cs.append(df_cap.iloc[len(df_cap)-1, ]
                      ["Shares Outstanding"]*threshold)
        cs_pos = pd.DataFrame(cs, index=thresholds)
    else:
        cs_pos = pd.DataFrame()
    return cs_pos

# combine the position of the participating, non-participating, and common shares,
# and return the combined dataframe


def combina_all_positions(part_pos, npart_pos, cs_pos):
    if npart_pos.empty:
        combined = pd.concat([part_pos, cs_pos], axis=1)
    elif part_pos.empty:
        combined = pd.concat([npart_pos, cs_pos], axis=1)
    else:
        combined = pd.concat([part_pos, npart_pos, cs_pos], axis=1)
    df_bp = pd.DataFrame(combined.sum(axis=1))
    return df_bp

# get all the break points, returrn the result in a dataframe


def get_all_bpft(df_bpft, df_bp):
    df_BT = pd.concat([df_bpft['BreakPoint To'], df_bp],
                      ignore_index=True).dropna()
    df_BF = pd.concat(
        [pd.DataFrame([np.nan], index=[0]), df_BT], ignore_index=True)
    df_BT.index = range(len(df_BT))
    df_BP = pd.concat([df_BF, df_BT], axis=1, ignore_index=True)
    df_BP.columns = ["BreakPoint From", "BreakPoint To"]
    df_BP = df_BP.fillna(0)
    return df_BP

# merge the breakpoints with the working cap_table


def merge_breakpoints(df_BP, df_cap):
    del df_cap['BreakPoint From']
    del df_cap['BreakPoint To']
    df_concat = pd.concat([df_cap, df_BP], axis=1)
    return df_concat

# aggregate all of the previous functions return the thresholds as
# a list, and the cap table as a dataframe


def aggregate_all_operations(df_cap):
    df_tmp = df_cap.copy()
    df_bpft = calculate_break_point(df_tmp)
    thresholds = get_sorted_threshold_lists(df_tmp)
    df_part_pos = get_participating_position(df_tmp, thresholds)
    df_npart_pos = get_non_participating_position(df_tmp, thresholds)
    df_cs_pos = get_common_share_position(df_tmp, thresholds)
    df_bp = combina_all_positions(df_part_pos, df_npart_pos, df_cs_pos)
    df_BP = get_all_bpft(df_bpft, df_bp)
    df_concat = merge_breakpoints(df_BP, df_tmp)
    return thresholds, df_concat, df_concat['BreakPoint From']
