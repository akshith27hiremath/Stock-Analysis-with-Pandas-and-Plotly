# https://github.com/akshith27hiremath/wallstreetinductionproject

import pandas as pd
import matplotlib as mpl
import numpy
import os

stock_dataset_filenames = [file for file in os.listdir("./datasets") if file.endswith('.csv')]
#print(stock_dataset_filenames)

stock_dataframes = []
for dataset in stock_dataset_filenames:
    stock_dataframes.append({"name": dataset[:-7], "data": pd.read_csv(dataset)}) ## include parameters we calculate as empty keys?

