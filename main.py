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

# print(stock_dataframes[0]['df'].ta.indicators())

for stock in stock_dataframes:
    df = stock["df"]
    numberofentries = len(df)
    print(f"{stock['name']} length is {numberofentries}")
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    df['RSI'] = ta.rsi(df['Close'], length = 14)

    df['MACD'], df['MACD_Signal'], df['MACD_Histogram'] = ta.macd(df['Close'], fast=12, slow=26, signal=9).iloc[:, 0:3].T.values

    bbands_df = ta.bbands(df['Close'], length=20, std=2)
    # df = pd.concat([df, bbands_df], axis=1)

    psar_df = ta.psar(df['High'], df['Low'], df['Close'], af=0.02, max_af=0.2)
    stock["psar_df"] = psar_df
    # psar_df = psar_df.reset_index()
    # psar_df = psar_df.drop('Date', axis=1)
    # df["PSARl_0.02_0.2"], df["PSARs_0.02_0.2"], df["PSARaf_0.02_0.2"], df["PSARr_0.02_0.2"] = psar_df

    (ichimoku_df_current, ichimoku_df_future) = ta.ichimoku(df['High'], df['Low'], df['Close'], tenkan=9, kijun=26, senkou=52)
    stock["ichimoku_df_current"] = ichimoku_df_current
    stock["ichimoku_df_future"] = ichimoku_df_future    # df = pd.concat([df, ichimoku_df_current], axis=1)
    # print(df.info())
    # print(df.columns)
    stock["df"] = df

for stock in stock_dataframes:
    stockname = stock["name"]
    df = stock["df"]
    ichimoku_df_current = stock["ichimoku_df_current"]
    ichimoku_df_future = stock["ichimoku_df_future"]
    psar_df = stock["psar_df"]
    os.mkdir(f"./output/{stockname}")
    df.to_csv(f"./output/{stockname}/rsimacdbbands.csv", index=True)
    ichimoku_df_current.to_csv(f"./output/{stockname}/ichimoku_df_current.csv", index=True)
    ichimoku_df_future.to_csv(f"./output/{stockname}/ichimoku_df_future.csv", index=True)
    psar_df.to_csv(f"./output/{stockname}/psar_df.csv", index=True)

