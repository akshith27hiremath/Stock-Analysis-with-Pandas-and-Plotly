# Pandas, Pandas_ta and Plotly to visualize and analyze stock close price data

## Prerequesites
Dataset csv files to be read in a folder in same directory `./datasets`
Python version used: 3.12.5 <br>
Libraries to be installed: pandas, pandas_ta (Latest Release, see below), plotly, ta, kaleido, numpy (1.26.4)<br> <br>

<b>Important: </b> pandas_ta uses an older version of numpy where "nan" was treated differently. <br>
<b>Set up a new virtualenv if numpy already exists on your system, then install pandas_ta using <b> <br> 
`pip install -U git+https://github.com/twopirllc/pandas-ta`

### Project Info
Uses <b>os</b> to automate the reading and writing of datasets and outputs. Uses pandas_ta, pandas, dictionaries and iteration to generate 6 informative technical analysis graphs for each stock.

## Setup
1. Clone the repository

```bash
git clone https://github.com/crux-bphc/bits-gpt.git
```

2. Create a virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

3. Install dependencies

```bash
pip uninstall numpy
pip install -U git+https://github.com/twopirllc/pandas-ta
pip install ta plotly kaleido
 pip install --upgrade setuptools
```

4. Move input data into correct folder

Copy stock dataset csv files into a folder in the the working directory. Enter the folder name into the main.py file, assigned to DATASETFOLDERNAME (default is "datasets")

4. Generate graphs
```bash
python main.py
```