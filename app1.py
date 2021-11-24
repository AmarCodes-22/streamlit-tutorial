import pandas as pd
import streamlit as st
import yfinance as yf

# st.write uses markdown syntax to write stuff
st.write("""
# Simple Stock Price App
Shown are the stock **closing price** and ***volume*** of Apple!

""")

ticker_symbol = 'AAPL'
ticker_data = yf.Ticker(ticker_symbol)
ticker_df = ticker_data.history(
    period='1d',
    start='2010-5-31',
    end='2020-5-31')

# writes a heading, makes an interactive line chart from the data
st.write("""
## Closing price
""")
st.line_chart(ticker_df.Close)

st.write("""
## Volume
""")
st.line_chart(ticker_df.Volume)
