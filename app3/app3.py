import base64

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import streamlit as st

st.title('NBA Player Stats Explorer')

# asterisk creates a bullet list
# double asterisk around text makes it Bold
# triple asterisk makes text italics
st.markdown("""
This app performs simple webscraping of NBA player stats data!
* **Python libraries:** base64, pandas, streamlit
* ***Data source:*** [Basketball-reference.com](https://www.basketball-reference.com/)
""")

st.sidebar.header('User Input Features')
selected_year = st.sidebar.selectbox('Year', list(reversed(range(1950,2020))))
# print(selected_year)

# Web scraping of NBA player stats
# st.cache caches the data, i can notice the difference when loading it 
# the first time vs loading it again
@st.cache
def load_data(year):
    url = "https://www.basketball-reference.com/leagues/NBA_" + str(year) + "_per_game.html"
    html = pd.read_html(url, header=0)
    df = html[0]
    raw = df.drop(df[df.Age == 'Age'].index)
    raw = raw.fillna(0)
    playerstats = raw.drop(['Rk'], axis=1)
    return playerstats
playerstats = load_data(selected_year)
st.write(playerstats)  # show dataframe

# Sidebar - team selection
sorted_unique_team = sorted(playerstats['Tm'].unique())

# allows multiple selections and returns a list
selected_team = st.sidebar.multiselect('Team', sorted_unique_team, sorted_unique_team)
# print(type(sorted_unique_team))

# Sidebar - position selection
uniq_pos = ['C','PF','SF','PG','SG']
selected_pos = st.sidebar.multiselect('Position', uniq_pos, uniq_pos)

df_selected_team = playerstats[
    (playerstats['Tm'].isin(selected_team)) &
    (playerstats['Pos'].isin(selected_pos))
    ]

st.header('Display player stats of selected team(s)')
st.write(
    'Data dimension: ' + 
    str(df_selected_team.shape[0]) +
    ' rows and ' +
    str(df_selected_team.shape[1]) + 
    ' columns')
st.dataframe(df_selected_team)

# download the dataframe
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv" > Download CSV File</a>'
    return href

st.markdown(filedownload(df_selected_team), unsafe_allow_html=True)

# Heatmap
if st.button('Generate Intercorrelation Heatmap'):
    st.header('Intercorrelation Matrix Heatmap')
    # print(type(df_selected_team))
    df_selected_team.to_csv('output.csv',index=False)
    df = pd.read_csv('output.csv')
    # print(type(df))

    corr = df.corr()
    mask = np.zeros_like(corr)
    mask[np.triu_indices_from(mask)] = True
    with sns.axes_style("white"):
        f, ax = plt.subplots(figsize=(7, 5))
        ax = sns.heatmap(corr, mask=mask, vmax=1, square=True)
    st.pyplot(f)
