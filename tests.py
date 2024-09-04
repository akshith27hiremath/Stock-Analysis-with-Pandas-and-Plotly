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

scores = []
for stock in output_dataframes:
    name = stock["name"]    
    last_valid_index = stock['rm']['RSI'].last_valid_index()

    closeprice = stock['rm'].loc[last_valid_index, 'Close']
    rsiscore = 100- stock["rm"].loc[last_valid_index, 'RSI'] 

    lowerband = stock['bbands'].loc[last_valid_index, 'BBL_20_2.0']
    upperband = stock['bbands'].loc[last_valid_index, 'BBU_20_2.0']

    bbandsscore = 100*(1-((closeprice-lowerband)/(upperband-lowerband)))

    scores.append({"name": name, "rsiscore": rsiscore, "bbandsscore": bbandsscore})
print(scores)