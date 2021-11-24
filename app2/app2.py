import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image
import matplotlib.pyplot as plt

#* Page title
image = Image.open('app2/dna-logo.jpg')
st.image(image, use_column_width=True)
st.write("""
# DNA Nucleotide count web app
This app counts the neucleotide composition of query DNA!
***
""")  # *** puts a horizonal divider

#* Input text box
st.header('Enter DNA sequence')

sequence_input = ">DNA Query 2\nGAACACGTGGAGGCAAACAGGAAGGTGAAGAAGAACTTATCCTATCAGGACGGAAGGTCCTGTGCTCGGG\nATCTTCCAGACGTCGCGACTCTAAATTGCCCCCTCTGAGGTCAAGGAACACAAGATGGTTTTGGAAATGC\nTGAACCCGATACATTATAACATCACCAGCATCGTGCCTGAAGCCATGCCTGCTGCCACCATGCCAGTCCT"

# the input in the text area gets stored in 'sequence' string
sequence = st.text_area("Sequence input", sequence_input, height=200)
sequence = sequence.split('\n')
sequence = sequence[1:]
sequence = ''.join(sequence)
print(f'sequence is of type {type(sequence)} and its length is {len(sequence)}')

# enters a horizontal divider
st.write("""***""")

#* Prints the input DNA sequence
st.header('INPUT {DNA Query}')

# we can just print the variable by putting it on a line like this
# (thanks to ipython)
sequence

#* DNA nucleotide count
st.header('OUTPUT {DNA Nucleotide Count}')

##* Print dictionary
st.subheader('1. Print as a dictionary')


def dna_nucleotide_count(seq):
    d = dict([
        ('A', seq.count('A')),
        ('T', seq.count('T')),
        ('G', seq.count('G')),
        ('C', seq.count('C')),
    ])
    return d


x = dna_nucleotide_count(sequence)
# these should be logs but we will let it be print statements for now
print(f'x is of type {type(x)}')
# x_label = list(x)
# x_values = list(x.values())
# printing the dictionary
st.write(x)

##* Print text
# you can use manual formatting of format strings with st.markdown
st.subheader('2. Print as text')
st.write('There are ' + str(x['A']) + ' adenine (A)')
st.write('There are ' + str(x['T']) + ' thymine (T)')
st.write('There are ' + str(x['G']) + ' guanine (G)')
st.write('There are ' + str(x['C']) + ' cytosine (C)')

##* Display as dataframe
st.subheader('3. Display as dataframe')
df = pd.DataFrame.from_dict(x, orient='index')
# df = df.rename(columns={0: 'count'}, axis='columns')
df = df.rename(columns={0: 'count'})
df.reset_index(inplace=True)
df = df.rename(columns={'index': 'nucleotide'})
# both of these work however i should use st.write to make it more clear
# df
st.write(df)

##* Display as barchart
st.subheader('4. Display as bar-chart (using altair)')
# using altair for bar-chart
p = alt.Chart(df).mark_bar().encode(
    x='nucleotide',
    y='count'
)
p = p.properties(
    width=alt.Step(60)  # changes the width of the bars
)
st.write(p)

# using matploblib
st.subheader('5. Display as bar-chart (using matplotlib)')
fig = plt.figure(figsize=(10, 5))
plt.bar(df['nucleotide'], df['count'])
st.pyplot(fig)

# altair seems to have better integration
# i can download the plot as image and stuff
