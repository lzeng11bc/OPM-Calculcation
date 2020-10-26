import pandas as pd
import numpy as np
from scipy.stats import norm


def getND1(equityValue, strikePrice,
           volatility, timeToLiquidity, rFrate, dividendYield):
    d1 = (np.log(equityValue/strikePrice)
          + (rFrate - dividendYield + 0.5 *
             volatility**2)*timeToLiquidity)/(volatility*np.sqrt(timeToLiquidity))
    Nd1 = norm.cdf(d1, 0.0, 1.0)
    return Nd1


def getND2(equityValue, strikePrice,
           volatility, timeToLiquidity, rFrate, dividendYield):
    d2 = (np.log(equityValue/strikePrice) + (rFrate - dividendYield -
                                             0.5*volatility**2) * timeToLiquidity)/(volatility*np.sqrt(timeToLiquidity))
    Nd2 = norm.cdf(d2, 0.0, 1.0)
    return Nd2


def getOptionPrice(Nd1, Nd2, strikePrice, equityValue, volatility, timeToLiqudity, rFrate, dividendYield):
    optionPrice = (equityValue*np.exp(-dividendYield*timeToLiqudity)) * \
        Nd1 - strikePrice*np.exp(-rFrate*timeToLiqudity)*Nd2
    return optionPrice


def get_incrementals(valuelist):
    incremntalvalueList = []
    num = len(valuelist)
    for i in range(num):
        if(i <= num-2):
            incremntalvalueList.append(
                valuelist[i]-valuelist[i+1])
        else:
            incremntalvalueList.append(valuelist[i])
    return incremntalvalueList


def get_nd1_list(df_cap, df_asm):
    nd1 = []
    for i in range(len(df_cap['BreakPoint From'])-1):
        nd1.append(getND1(df_asm['Equity Value'], df_cap['BreakPoint From'][i],
                          df_asm['Expected volatility'],
                          df_asm['Expected time to liquidation'],
                          df_asm['Risk-free Rate'],
                          df_asm['Expected Dividend Yield']))
    return nd1


def get_nd2_list(df_cap, df_asm):
    nd2 = []
    for i in range(len(df_cap['BreakPoint From'])-1):
        nd2.append(getND2(df_asm['Equity Value'], df_cap['BreakPoint From'][i],
                          df_asm['Expected volatility'],
                          df_asm['Expected time to liquidation'],
                          df_asm['Risk-free Rate'],
                          df_asm['Expected Dividend Yield']))
    return nd2


def get_option_price_list(df_cap, df_asm, nd1, nd2):
    optionprice = []
    for i in range(len(df_cap['BreakPoint From'])-1):
        optionprice.append(getOptionPrice(
            nd1[i],
            nd2[i],
            df_cap['BreakPoint From'][i],
            df_asm['Equity Value'],
            df_asm['Expected volatility'],
            df_asm['Expected time to liquidation'],
            df_asm['Risk-free Rate'],
            df_asm['Expected Dividend Yield']
        )
        )
    return optionprice


def get_incremental_value(optionprice):
    incremental_value_list = get_incrementals(optionprice)
    return incremental_value_list


def get_opm_table(nd1, nd2, optionprice, incremental_value_list):
    df_opm = pd.DataFrame(
        {'ND1': nd1, 'ND2': nd2, 'Option Price Computation': optionprice, 'Incremental Value': incremental_value_list})
    return df_opm


def get_total_opm(df_concat, df_asm):
    nd1 = get_nd1_list(df_concat, df_asm)
    nd2 = get_nd2_list(df_concat, df_asm)
    optionprice = get_option_price_list(df_concat, df_asm, nd1, nd2)
    incremental_value_list = get_incremental_value(optionprice)
    df_opm = get_opm_table(nd1, nd2, optionprice, incremental_value_list)
    return optionprice, incremental_value_list, df_opm
