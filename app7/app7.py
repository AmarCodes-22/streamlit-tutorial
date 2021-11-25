import pandas as pd
from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
import streamlit as st

st.write("""
# Simple Iris Flower Prediction App
This app predicts the Iris flower type
""")

# do work inside sidebar
with st.sidebar:
    st.header('User input features')
    sepal_length = st.slider('sepal_length', 4.3, 7.9, 5.4)
    sepal_width = st.slider('sepal_width', 2.0, 4.4, 3.4)
    petal_length = st.slider('petal_length', 1.0, 6.9, 1.3)
    petal_width = st.slider('petal_width', 0.1, 2.5, 0.2)
    data = dict()
    data['sepal_length'] = sepal_length
    data['sepal_width'] = sepal_width
    data['petal_length'] = petal_length
    data['petal_width'] = petal_width
    features = pd.DataFrame(data, index=[0])

# show the dataframe
st.markdown('### User input features')
st.dataframe(features)

# load dataset iris
iris = datasets.load_iris()  # returns a sklearn.utils.Bunch object
X, Y = iris.data, iris.target  # returns two numpy arrays

# make classifier
clf = RandomForestClassifier()  # instantiates the clf
clf.fit(X, Y)  # tweaks the random forest to fit the data distribution

# get predictions from the trained classifier
prediction = clf.predict(features)
prediction_prob = clf.predict_proba(features)

# show class labels and their indices
st.markdown('### Class labels and their corresponding index number')
st.write(iris.target_names)  # can write numpy arrays that look like dataframe

# show prediction
st.markdown('### Prediction')
st.write(iris.target_names[prediction])  # shows numpy array as dataframe

# show prediction probability
st.markdown('### Prediction probability')
st.write(prediction_prob)
