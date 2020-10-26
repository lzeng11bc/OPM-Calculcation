import pandas as pd
import numpy as np

# make a opm setting function to test various cases


def opm_setter(equity_value, r_f_rate=1e-20, volitility=1e-15,
               divyield=0, time_to_liquidation=1e-12):
    df_asm = pd.Series({'Equity Value': equity_value,
                        'Risk-free Rate': r_f_rate,
                        'Expected volatility': volitility,
                        'Expected Dividend Yield': divyield,
                        'Valuation Date': '31-Dec-19',
                        'End Date': '31-Dec-25',
                        'Expected time to liquidation': time_to_liquidation})
    return df_asm
