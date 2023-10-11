import os
import numpy as np
import pandas as pd
import akshare as ak
import matplotlib.pyplot as plt
import mplfinance as mpf
from datetime import datetime

df = ak.stock_zh_a_hist(symbol='600318',start_date='20221001',end_date='20231031',adjust="qfq");
print(df)

df.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 'value', '振幅','涨跌幅','涨跌额','换手率']

df.index = pd.DatetimeIndex(df['date'])
 
# data.head
mc = mpf.make_marketcolors(up='r',down='g')
s  = mpf.make_mpf_style(marketcolors=mc,mavcolors=['#4f8a8b','#fbd46d','#87556f'])
 
mpf.plot(df, type='candle')



#print(pd);

mpf.plot(pd,type='line')

#sz_index = ak.stock_zh_index_daily(symbol="sh000001")
#print(sz_index)
