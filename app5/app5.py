import base64

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st
import yfinance as yf

# title of the webpage
st.title('S&P 500 App')

# double asterisk makes text bold, triple makes it elastic
st.markdown("""
This app retrieves the list of the **S&P 500** (from Wikipedia) and its corresponding **stock closing price** (year-to-date)!
* **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn
* **Data source:** [Wikipedia](https://en.wikipedia.org/wiki/List_of_S%26P_500_companies).
""")

# Creates a toggle sidebar
st.sidebar.header('User Input Features')

# Web scraping the data from wikipedia
# st.cache caches data when it is downloaded for the first time
@st.cache
def load_data():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    # reads tables from the webpage and returns a list of dataframes
    html = pd.read_html(url, header=0)

    df = html[0]
    return df

# saves the table in a dataframe
df = load_data()

# creates a pandas groupby object
sector = df.groupby('GICS Sector')

# sidebar - sector selection
# creates a list of all sectors
sorted_sector_unique = sorted(df['GICS Sector'].unique())
# stores the selection of the sidebar in a list
selected_sector = st.sidebar.multiselect(
    'Sector',
    sorted_sector_unique,
    sorted_sector_unique)

# filtering data
# stores data about selected sectors in a dataframe
df_selected_sector = df[df['GICS Sector'].isin(selected_sector)]

st.header('Display Companies in selected sectors')
st.write(
    'Data dimension: ' +
    str(df_selected_sector.shape[0]) +
    ' rows and ' +
    str(df_selected_sector.shape[1]) +
    ' columns')
st.dataframe(df_selected_sector)

# download S&P500 data
def filedownload(df):
    # converts the dataframe to a str
    csv = df.to_csv(index=False)
    # print(csv[:300])

    # csv.encode() converts the str to binary string
    # base64.b64encode() converts the str to base64 encoding
    b64 = base64.b64encode(csv.encode()).decode()

    href = f'<a href="data:file/csv;base64,{b64}" download="SP500.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_sector), unsafe_allow_html=True)

# download data from yfinance about selected sectors
data = yf.download(
    tickers = list(df_selected_sector[:10]['Symbol']),
    period = 'ytd',
    interval = '1wk',
    group_by = 'ticker',
    auto_adjust = True,
    prepost = True,
    threads = True,
    proxy = None
)

# plot closing price of query symbol
st.set_option('deprecation.showPyplotGlobalUse', False)
def price_plot(symbol):
    df = pd.DataFrame(data[symbol]['Close'])
    df['Date'] = df.index
    # fig, ax = plt.subplots(figsize=(15,5))
    plt.fill_between(df['Date'], df['Close'], color='skyblue', alpha=0.3)
    plt.plot(df['Date'], df['Close'], color='skyblue', alpha=0.8)
    plt.xticks(rotation=90)
    plt.title(symbol, fontweight='bold')
    plt.xlabel('Date', fontweight='bold')
    plt.ylabel('Closing price', fontweight='bold')
    return st.pyplot()

# makes a slider
num_company = st.sidebar.slider('Number of companies', 1, 5)

# make a button to show the plots
if st.button('Show plots'):
    st.header('Stock closing price')
    for i in list(df_selected_sector['Symbol'])[:num_company]:
        price_plot(i)
