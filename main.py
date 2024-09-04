# https://github.com/akshith27hiremath/wallstreetinductionproject

import pandas as pd
import matplotlib as mpl
import numpy
import os
import pandas_ta as ta

stock_dataset_filenames = [file for file in os.listdir("./datasets") if file.endswith('.csv')]

stock_dataframes = []
for dataset in stock_dataset_filenames:
    stock_dataframes.append({"name": dataset[:-7], "df": pd.read_csv(f"./datasets/{dataset}")})

for stock in stock_dataframes:
    df = stock["df"]
    numberofentries = len(df)
    print(f"{stock['name']} length is {numberofentries}")
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)

    df['RSI'] = ta.rsi(df['Close'], length = 14)

    df['MACD'], df['MACD_Signal'], df['MACD_Histogram'] = ta.macd(df['Close'], fast=12, slow=26, signal=9).iloc[:, 0:3].T.values

    bbands_df = ta.bbands(df['Close'], length=20, std=2)
    stock['bbands_df'] = bbands_df

    psar_df = ta.psar(df['High'], df['Low'], df['Close'], af=0.02, max_af=0.2)
    
    psar_df["PSAR"] = None
    initial_trend = 'up' if psar_df['PSARl_0.02_0.2'].iloc[0] == 1 else 'down'
    EP = df['Close'].iloc[0]
    AF = psar_df['PSARaf_0.02_0.2'].iloc[0]
    PSAR = df['Close'].iloc[0]  # Example start
    for i in range(1, len(df)):
        if initial_trend == 'up':
            PSAR = PSAR + AF * (EP - PSAR)
            if df['Close'].iloc[i] < PSAR:  # Reversal condition
                initial_trend = 'down'
                PSAR = EP  # Reset to previous EP
                AF = psar_df['PSARaf_0.02_0.2'].iloc[i]  # Reset AF
                EP = df['Close'].iloc[i]  # Update EP for the downtrend
            else:
                EP = max(EP, df['Close'].iloc[i])
                AF = min(AF + 0.02, 0.20)  # Increase AF with a cap

        elif initial_trend == 'down':
            PSAR = PSAR - AF * (PSAR - EP)
            if df['Close'].iloc[i] > PSAR:  # Reversal condition
                initial_trend = 'up'
                PSAR = EP  # Reset to previous EP
                AF = psar_df['PSARaf_0.02_0.2'].iloc[i]  # Reset AF
                EP = df['Close'].iloc[i]  # Update EP for the uptrend
            else:
                EP = min(EP, df['Close'].iloc[i])
                AF = min(AF + 0.02, 0.20)  # Increase AF with a cap

        psar_df['PSAR'].iloc[i] = PSAR  # Save the current PSAR value
    stock["psar_df"] = psar_df
    (ichimoku_df_current, ichimoku_df_future) = ta.ichimoku(df['High'], df['Low'], df['Close'], tenkan=9, kijun=26, senkou=52)
    stock["ichimoku_df_current"] = ichimoku_df_current
    stock["ichimoku_df_future"] = ichimoku_df_future    # df = pd.concat([df, ichimoku_df_current], axis=1)
    # print(df.info())
    # print(df.columns)
    stock["df"] = df
os.mkdir(f"./output")
for stock in stock_dataframes:
    stockname = stock["name"]
    df = stock["df"]
    ichimoku_df_current = stock["ichimoku_df_current"]
    ichimoku_df_future = stock["ichimoku_df_future"]
    psar_df = stock["psar_df"]
    bbands_df = stock["bbands_df"]
    os.mkdir(f"./output/{stockname}")
    df.to_csv(f"./output/{stockname}/rsimacd_df.csv", index=True)
    ichimoku_df_current.to_csv(f"./output/{stockname}/ichimoku_df_current.csv", index=True)
    ichimoku_df_future.to_csv(f"./output/{stockname}/ichimoku_df_future.csv", index=True)
    psar_df.to_csv(f"./output/{stockname}/psar_df.csv", index=True)
    bbands_df.to_csv(f"./output/{stockname}/bbands_df.csv", index=True)

