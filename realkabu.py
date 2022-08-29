import pandas as pd
import sys
import matplotlib.pyplot as plt
from matplotlib import dates as mdates
import datetime as dt

from yahoo_finance_api2 import share
from yahoo_finance_api2.exceptions import YahooFinanceError

# 日本株については.Tをつける：code + ".T"個別株
share_list = ['AAPL','IBM','KO','PG','T','6861.T']

for w in share_list:
    symbol_data = None
    my_share = share.Share(w)

    try:
        symbol_data = my_share.get_historical(
            share.PERIOD_TYPE_DAY, 10,
            share.FREQUENCY_TYPE_MINUTE, 5)
    except YahooFinanceError as e:
        print(e.message)
        sys.exit(1)

    df = pd.DataFrame(symbol_data)
    
    df["datetime"] = pd.to_datetime(df.timestamp, unit="ms")

    #日本時間へ変換
    df["datetime_JST"] = df["datetime"] + dt.timedelta(hours=9)

    set_df = df.set_index('datetime_JST') 

    print(set_df["datetime"].dt.dayofweek)

    set_df["close"].plot(grid = True)
    plt.show()
