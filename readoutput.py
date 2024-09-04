import pandas as pd
import plotly.graph_objs as go
import os

stock_dataset_filenames = [file for file in os.listdir("./datasets") if file.endswith('.csv')]
stock_names = [file[:-7] for file in stock_dataset_filenames]

print(stock_names)
output_dataframes = []

for name in stock_names:
    output = {}
    output["name"] = name
    output["rm"] = pd.read_csv(f"./output/{name}/rsimacd_df.csv")
    output["psar"] = pd.read_csv(f"./output/{name}/psar_df.csv")
    output["ichimoku_df_current"] = pd.read_csv(f"./output/{name}/ichimoku_df_current.csv")
    output["ichimoku_df_future"] = pd.read_csv(f"./output/{name}/ichimoku_df_future.csv")
    output["bbands"] = pd.read_csv(f"./output/{name}/bbands_df.csv")
    output_dataframes.append(output)

def rsigenerate(df, name):
    rsi_trace = go.Scatter(x=df['Date'], y=df['RSI'], mode='lines', name='RSI', line=dict(color='blue'))
    overbought_line = go.Scatter(x=df['Date'], y=[70] * len(df), mode='lines', name='Overbought (70)', line=dict(color='red', dash='dash'))
    oversold_line = go.Scatter(x=df['Date'], y=[30] * len(df), mode='lines', name='Oversold (30)', line=dict(color='green', dash='dash'))
    rsi_fig = go.Figure(data=[rsi_trace, overbought_line, oversold_line])
    rsi_fig.update_layout(title=f'Relative Strength Index (RSI) of {name}', xaxis_title='Date', yaxis_title='RSI Value',yaxis=dict(range=[0, 100]), template='plotly_dark')
    return(rsi_fig)

def macdgenerate(df, name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'],y=df['MACD'],name='MACD Line',line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['MACD_Signal'],name='Signal Line',line=dict(color='red')))
    fig.add_trace(go.Bar(x=df['Date'],y=df['MACD_Histogram'],name='MACD Histogram',marker=dict(color='green' if df['MACD_Histogram'].iloc[-1] > 0 else 'red')))
    fig.update_layout(title=f'MACD of f{name}',xaxis_title='Date',yaxis_title='Value',barmode='relative',  height=600,template='plotly_dark')
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

def ichimokufuturegenerate(df, closedf, name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'],y=closedf['Close'],name='Close Price',line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['ISA_9'],name='Senkou Span A (Leading Span A)',line=dict(color='orange'),fill=None))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['ISB_26'],name='Senkou Span B (Leading Span B)',line=dict(color='purple'),fill='tonexty',fillcolor='rgba(128, 0, 128, 0.2)'))
    fig.update_layout(title=f'Ichimoku Cloud with Future Clouds of {name}',xaxis_title='Date',yaxis_title='Price',height=600,template='plotly_dark')
    return(fig)

def ichimokucurrentgenerate(df, closedf, name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'],y=closedf['Close'],name='Close Price',line=dict(color='blue')))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['ITS_9'],name='Tenkan-sen (Conversion Line)',line=dict(color='red', dash='dash')))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['IKS_26'],name='Kijun-sen (Base Line)',line=dict(color='green', dash='dash')))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['ISA_9'],name='Senkou Span A (Leading Span A)',line=dict(color='orange'),fill=None))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['ISB_26'],name='Senkou Span B (Leading Span B)',line=dict(color='purple'),fill='tonexty',fillcolor='rgba(128, 0, 128, 0.2)'))
    fig.add_trace(go.Scatter(x=df['Date'],y=df['ICS_26'],name='Chikou Span (Lagging Span)',line=dict(color='grey', dash='dot')))
    fig.update_layout(title=f'Ichimoku Cloud with Current Clouds of {name}',xaxis_title='Date',yaxis_title='Price',height=600,template='plotly_dark')
    return(fig)


def psargenerate(df, closedf, name):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['Date'], y=closedf['Close'], mode='lines', name='Close'))
    fig.add_trace(go.Scatter(x=df['Date'], y=df['PSAR'], mode='markers', name='Parabolic SAR', marker=dict(color='blue', size=6)))
    fig.add_trace(go.Scatter(x=df[df['PSARl_0.02_0.2'] == 1]['Date'], y=closedf[df['PSARl_0.02_0.2'] == 1]['Close'], mode='markers', name='Long', marker=dict(color='green', size=8, symbol='triangle-up')))
    fig.add_trace(go.Scatter(x=df[df['PSARs_0.02_0.2'] == -1]['Date'], y=closedf[df['PSARs_0.02_0.2'] == -1]['Close'], mode='markers', name='Short', marker=dict(color='red', size=8, symbol='triangle-down')))
    fig.add_trace(go.Scatter(x=df[df['PSARr_0.02_0.2'] != 0]['Date'], y=closedf[df['PSARr_0.02_0.2'] != 0]['Close'], mode='markers', name='Reversal', marker=dict(color='orange', size=8, symbol='diamond')))
    fig.update_layout(title=f'Parabolic SAR of {name}', xaxis_title='Date', yaxis_title='Price', xaxis_rangeslider_visible=False, template='plotly_dark')
    return(fig)



def write_outputs():
    for stock in output_dataframes:
        name = stock["name"]
        rsimacd = stock["rm"]
        psardf = stock["psar"]
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
        ichimokufuturetgraph = ichimokucurrentgenerate(ichimokufuturedf, rsimacd, name)
        ichimokufuturetgraph.write_image(f"{save_dir}ichimokufuture.png")
        psargraph = psargenerate(psardf, rsimacd, name)
        psargraph.write_image(f"{save_dir}psar.png")

# write_outputs()

def comparative_analysis():
    scores = []
    for stock in output_dataframes:
        name = stock["name"]
        rsiscore = 100-stock["rm"]