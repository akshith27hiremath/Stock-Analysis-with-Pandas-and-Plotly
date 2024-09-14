# https://github.com/akshith27hiremath/wallstreetinductionproject

import pandas as pd
import os
import pandas_ta as pta
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import ta
import ta.momentum
import ta.trend
import shutil

COMMONTRAILINGCHARACTERS = ".NS.csv"
DATASETFOLDERNAME = "datasets"

stock_dataset_filenames = [file for file in os.listdir(f"./{DATASETFOLDERNAME}") if file.endswith('.csv')] # use os to automatically iterate
stock_dataframes = []

for dataset in stock_dataset_filenames:
    stock_dataframes.append({"name": dataset[:-len(COMMONTRAILINGCHARACTERS)], "df": pd.read_csv(f"./{DATASETFOLDERNAME}/{dataset}")}) # shortern string by eliminating common characters
stock_names = [file[:-7] for file in stock_dataset_filenames]
print(stock_names)

for stock in stock_dataframes:
    df = stock["df"]
    numberofentries = len(df)
    print(f"{stock['name']} length is {numberofentries}")
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df['RSI'] = pta.rsi(df['Close'], length = 14)
    df['MACDcolumn'], df['MACD_Signal'], df['MACD_Histogram'] = pta.macd(df['Close'], fast=12, slow=26, signal=9).iloc[:, 0:3].T.values
    bbands_df = pta.bbands(df['Close'], length=20, std=2)
    stock['bbands_df'] = bbands_df
    (ichimoku_df_current, ichimoku_df_future) = pta.ichimoku(df['High'], df['Low'], df['Close'], tenkan=9, kijun=26, senkou=52)
    stock['ichimoku_df_current'] = ichimoku_df_current
    stock['ichimoku_df_future'] = ichimoku_df_future    # df = pd.concat([df, ichimoku_df_current], axis=1)
    # print(df.info())
    # print(df.columns)
    stock["df"] = df

shutil.rmtree("./output", ignore_errors=True)
os.mkdir(f"./output")

for stock in stock_dataframes:
    stockname = stock['name']
    df = stock['df']
    ichimoku_df_current = stock['ichimoku_df_current']
    ichimoku_df_future = stock['ichimoku_df_future']
    # psar_df = stock['psar_df']
    bbands_df = stock['bbands_df']
    os.mkdir(f"./output/{stockname}")
    df.to_csv(f"./output/{stockname}/rsimacd_df.csv", index=True)
    ichimoku_df_current.to_csv(f"./output/{stockname}/ichimoku_df_current.csv", index=True)
    ichimoku_df_future.to_csv(f"./output/{stockname}/ichimoku_df_future.csv", index=True)
    # psar_df.to_csv(f"./output/{stockname}/psar_df.csv", index=True)
    bbands_df.to_csv(f"./output/{stockname}/bbands_df.csv", index=True)


output_dataframes = []

for name in stock_names:
    output = {}
    output['name'] = name
    output['rm'] = pd.read_csv(f"./output/{name}/rsimacd_df.csv")
    # output["psar"] = pd.read_csv(f"./output/{name}/psar_df.csv")
    output['ichimoku_df_current'] = pd.read_csv(f"./output/{name}/ichimoku_df_current.csv")
    output['ichimoku_df_future'] = pd.read_csv(f"./output/{name}/ichimoku_df_future.csv")
    output['bbands'] = pd.read_csv(f"./output/{name}/bbands_df.csv")
    output_dataframes.append(output)

def rsigenerate(df, name):
    fig = go.Figure()
    rsi_trace = go.Scatter(x=df['Date'], y=df['RSI'], mode='lines', name='RSI', line=dict(color='blue'))
    # close_line = go.Scatter(x=df['Date'],y=df['Close'],name='Close Price',line=dict(color='white'))
    overbought_line = go.Scatter(x=df['Date'], y=[70] * len(df), mode='lines', name='Overbought (70)', line=dict(color='red', dash='dash'))
    oversold_line = go.Scatter(x=df['Date'], y=[30] * len(df), mode='lines', name='Oversold (30)', line=dict(color='green', dash='dash'))
    fig.add_trace(rsi_trace)
    # fig.add_trace(rsi_trace)
    fig.add_trace(overbought_line)
    fig.add_trace(oversold_line)
    fig.update_layout(title=f'Relative Strength Index (RSI) of {name}', xaxis_title='Date', yaxis_title='RSI Value',yaxis=dict(range=[0, 100]), template='plotly_dark')
    return(fig)

def macdgenerate(df, name):
    df['12expmovingaverage'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['26expmovingaverage'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['12expmovingaverage'] - df['26expmovingaverage']
    df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
    df['Histogram'] = df['MACD'] - df['Signal']
    fig = make_subplots(rows=1, cols=1, shared_xaxes=True, subplot_titles=('MACD'))
    fig.add_trace(go.Scatter(x=df["Date"],y=df['MACD'],mode='lines',name='MACD',line=dict(color='blue')), row=1, col=1)
    fig.add_trace(go.Scatter(x=df["Date"],y=df['Signal'],mode='lines',name='Signal',line=dict(color='red')), row=1, col=1)
    fig.add_trace(go.Bar(x=df["Date"],y=df['Histogram'],name='MACD Histogram',marker_color=(df['Histogram'] > 0).map({True: 'green', False: 'red'})), row=1, col=1)
    fig.update_layout(title=f'MACD of {name}',xaxis_title='Date',yaxis_title='Price',xaxis_rangeslider_visible=False,height=800,width=1000, template='plotly_dark')
    return(fig)

def bbandsgenerate(df, closedf, name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'],y=closedf['Close'],name='Close Price',line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['BBU_20_2.0'],name='Upper Band',line=dict(color='orange'),fill=None))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['BBL_20_2.0'],name='Lower Band',line=dict(color='orange'),fill='tonexty',fillcolor='rgba(255, 165, 0, 0.2)'))
    if 'BBM_20_2.0' in df.columns:
        fig.add_trace(go.Scatter(x=df['Date'],y=df['BBM_20_2.0'],name='Middle Band (MA)',line=dict(color='green', dash='dash')))
    fig.update_layout(title=f'Bollinger Bands of {name}',xaxis_title='Date',yaxis_title='Price',height=600,template='plotly_dark')
    return(fig)


def ichimokucurrentgenerate(df, closedf, name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'],y=closedf['Close'],name='Close Price',line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['ITS_9'],name='Tenkan-sen (Conversion Line)',line=dict(color='white', dash='dash')))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['IKS_26'],name='Kijun-sen (Base Line)',line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['ISA_9'],name='Senkou Span A (Leading Span A)',line=dict(color='green'),fill=None))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['ISB_26'],name='Senkou Span B (Leading Span B)',line=dict(color='brown'),fill='tonexty',fillcolor='rgba(0, 100, 80, 0.2)'))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['ICS_26'],name='Chikou Span (Lagging Span)',line=dict(color='grey', dash='dot')))
    fig.update_layout(title=f'Ichimoku Cloud with Current Clouds of {name}',xaxis_title='Date',yaxis_title='Price',height=600,template='plotly_dark')
    return(fig)

def closegeneratedark(df, name):
    fig = go.Figure()
    fig.add_trace(go.Candlestick(x=df.index,open=df['Open'],high=df['High'],low=df['Low'],close=df['Close'],name='Candlesticks'))
    fig.update_layout(title=f'Candlesticks of {name}',xaxis_title='Date',yaxis_title='Price',height=600,template='plotly_dark',xaxis_rangeslider_visible=False, width=1500)
    return(fig)

def psargenerate(closedf, name):
    # fig = go.Figure()
    # fig.add_trace(go.Candlestick(x=df['Date'], close=closedf['Close'], name='Close'))
    # fig.add_trace(go.Scatter(x=df['Date'], y=df['PSAR'], mode='markers', name='Parabolic SAR', marker=dict(color='blue', size=6)))
    # fig.add_trace(go.Scatter(x=df[df['PSARl_0.02_0.2'] == 1]['Date'], y=closedf[df['PSARl_0.02_0.2'] == 1]['Close'], mode='markers', name='Long', marker=dict(color='green', size=8, symbol='triangle-up')))
    # fig.add_trace(go.Scatter(x=df[df['PSARs_0.02_0.2'] == -1]['Date'], y=closedf[df['PSARs_0.02_0.2'] == -1]['Close'], mode='markers', name='Short', marker=dict(color='red', size=8, symbol='triangle-down')))
    # fig.add_trace(go.Scatter(x=df[df['PSARr_0.02_0.2'] != 0]['Date'], y=closedf[df['PSARr_0.02_0.2'] != 0]['Close'], mode='markers', name='Reversal', marker=dict(color='orange', size=8, symbol='diamond')))
    # fig.update_layout(title=f'Parabolic SAR of {name}', xaxis_title='Date', yaxis_title='Price', xaxis_rangeslider_visible=False, template='plotly_dark')
    # return(fig)
    closedf['psar'] = ta.trend.PSARIndicator(closedf['High'] , closedf['Low'] , closedf['Close'] , 0.02 , 0.02 , fillna=False).psar()
    fig = go.Figure(data=[go.Candlestick(x=closedf.index,open=closedf['Open'],high=closedf['High'],                                        low=closedf['Low'],close=closedf['Close'],name='Candlesticks')])
    fig.add_trace(go.Scatter(x=closedf.index, y=closedf['psar'],mode='markers',marker=dict(color='red', size=5),name='PSAR'))
    fig.update_layout(title=f'PSAR of {name}',xaxis_title='',yaxis_title='Price',xaxis_rangeslider_visible=False, template='plotly_dark')
    return(fig)

def write_outputs():
    for stock in output_dataframes:
        name = stock["name"]
        rsimacd = stock["rm"]
        # psardf = stock["psar"]
        bbands = stock["bbands"]
        ichimokucurrentdf = stock["ichimoku_df_current"]
        ichimokufuturedf = stock["ichimoku_df_current"]
        save_dir = f"./output/{name}/graphs/"
        os.mkdir(save_dir)
        rsigraph = rsigenerate(rsimacd, name)
        rsigraph.write_image(f"{save_dir}rsi.png")
        bbandsgraph = bbandsgenerate(bbands, rsimacd, name)
        bbandsgraph.write_image(f"{save_dir}bbands.png")
        macdgraph = macdgenerate(rsimacd, name)
        macdgraph.write_image(f"{save_dir}macd.png")
        ichimokucurrentgraph = ichimokucurrentgenerate(ichimokucurrentdf, rsimacd, name)
        ichimokucurrentgraph.write_image(f"{save_dir}ichimokucurrent.png")
        # ichimokufuturetgraph = ichimokucurrentgenerate(ichimokufuturedf, rsimacd, name)
        # ichimokufuturetgraph.write_image(f"{save_dir}ichimokufuture.png")
        psargraph = psargenerate(rsimacd, name)
        psargraph.write_image(f"{save_dir}psar.png")
        closedark = closegeneratedark(rsimacd, name)
        closedark.write_image(f"{save_dir}closedark{name}.png")
        """closelight = closegeneratelight(rsimacd, name)
        closelight.write_image(f"{save_dir}closelight{name}.png")"""

write_outputs()