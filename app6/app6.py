import base64
import json
from PIL import Image
from pprint import pprint
import requests
import time

from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
# import numpy as np
import pandas as pd
# import seaborn as sns
import streamlit as st

# setting the config to use the whole width of webpage
st.set_page_config(layout="wide")

# showing the image
image = Image.open('logo.jpg')
st.image(image, width=500)

st.title('Crypto price app')
st.markdown("""
This app retrieves cryptocurrency prices for the top 100 cryptocurrency from the **CoinMarketCap**!
""")

# Collapsible section
with st.expander("About"):
    st.write("""
    * **Python libraries:** base64, pandas, streamlit, numpy, matplotlib, seaborn, BeautifulSoup, requests, json, time
    * **Data source:** [CoinMarketCap](http://coinmarketcap.com).
    """)

# creating columns
col1 = st.sidebar
col2, col3 = st.columns((2,1))

col1.header('Input options')
currency_price_unit = col1.selectbox(
    'Select currency for price',
    ('USD', 'BTC', 'ETH'))

# Web scraping of CoinMarketCap data
@st.cache
def load_data():
    cmc = requests.get('https://coinmarketcap.com')
    soup = BeautifulSoup(cmc.content, 'html.parser')

    data = soup.find('script', id='__NEXT_DATA__', type='application/json')
    coins = {} 
    coins_data = json.loads(data.contents[0])
    currencies = coins_data['props']['initialState']['cryptocurrency']['listingLatest']['data']

    # see the key-index map
    # for i, key in enumerate(currencies[0]['keysArr']):
    #     print(i, key, sep='|')

    # dataframe columns
    coin_name = []
    coin_symbol = []
    market_cap = []
    price = []
    # percent_change_1h = []
    # percent_change_24h = []
    # percent_change_7d = []
    # volume_24h = []

    # populate lists
    for i, currency in enumerate(currencies):
        # changed keys to indices and key-index map is in index 0
        if i == 0:
            continue
        coin_name.append(currency[125])
        coin_symbol.append(currency[126])
        market_cap.append(currency[73])
        price.append(currency[100])

    # turn into dataframe
    df = pd.DataFrame(columns=['coin_name','coin_symbol','market_cap','price'])
    df['coin_name'] = coin_name
    df['coin_symbol'] = coin_symbol
    df['price'] = price
    df['market_cap'] = market_cap

    return df

df = load_data()

# Maybe i will try this later
# with st.sidebar:
#     st.header('Col1')
# with col2:
#     st.header('Col2')
# with col3:
#     st.header('Col3')
