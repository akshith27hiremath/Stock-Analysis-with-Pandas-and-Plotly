# https://github.com/akshith27hiremath/wallstreetinductionproject

import pandas as pd
import matplotlib as mpl
import numpy
import os
# from talipp.ohlcv import OHLCV
# from talipp.indicators import RSI
import pandas_ta as ta

stock_dataset_filenames = [file for file in os.listdir("./datasets") if file.endswith('.csv')]
#print(stock_dataset_filenames)

stock_dataframes = []
for dataset in stock_dataset_filenames:
    stock_dataframes.append({"name": dataset[:-7], "df": pd.read_csv(f"./datasets/{dataset}")}) ## include parameters we calculate as empty keys?

print(stock_dataframes[0]['df'].ta.indicators())

for stock in stock_dataframes:
    df = stock["df"]
    numberofentries = len(df)
    print(f"{stock['name']} length is {numberofentries}")
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    df['RSI'] = ta.rsi(df['Close'], length = 14)

    df['MACD'], df['MACD_Signal'], df['MACD_Histogram'] = ta.macd(df['Close'], fast=12, slow=26, signal=9).iloc[:, 0:3].T.values

    bbands_df = ta.bbands(df['Close'], length=20, std=2)
    df = pd.concat([df, bbands_df], axis=1)

    # df['Parabolic_SAR'] = ta.psar(df['High'], df['Low'], df['Close'], af=0.02, max_af=0.2)
    psar_df = ta.psar(df['High'], df['Low'], df['Close'], af=0.02, max_af=0.2)
    print(psar_df.head())
    # df['Parabolic_SAR'] = psar_df['PSAR']
    # df['PSARl'] = psar_df['PSARl']
    # df['PSARs'] = psar_df['PSARs']

    # ichimoku_df = ta.ichimoku(df['High'], df['Low'], df['Close'], tenkan=9, kijun=26, senkou=52)
    # # df = pd.concat([df, ichimoku_df], axis=1)
    # ichimoku_df.head

# for stock in stock_dataframes:
#     stockname = stock["name"]
#     df = stock["df"]
#     df.to_csv(f"./output/{stockname}", index=False)

