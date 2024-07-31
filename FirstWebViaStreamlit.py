path = 'cd' + r'C:\Users\ptfrey\Music\Github\WebDev'

# On a CMD prompt i need the folowing code to run this Site python -m streamlit run FirstWebViaStreamlit.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

#Initial config of page

st.set_page_config(page_title="My First Web Page!", page_icon=":tada:",layout="wide")


#Header section
st.subheader("Hello Guys! I'm a developer")
st.title("I Develop data visuals using PowerBI")
st.write("There are many other thing that I enjoy")
st.write("[Learn More>](https://www.google.com.br)")

# Sidebar for user inputs
st.sidebar.header("User Inputs")
num_points = st.sidebar.slider("Number of points", min_value=100, max_value=1000, value=500)
random_seed = st.sidebar.number_input("Random seed", value=42)

# Generate random data
np.random.seed(random_seed)
data = pd.DataFrame({
    'x1': np.random.randn(num_points),
    'x2': np.random.randn(num_points),
    'y': np.random.randn(num_points)
})

# Display data summary
st.header("Data Summary")
st.write(data.describe())

# Plotting
st.header("Data Visualizations")

# Scatter plot
st.subheader("Scatter Plot")
scatter_col1, scatter_col2 = st.columns(2)
with scatter_col1:
    st.write("X1 vs Y")
    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x='x1', y='y', ax=ax)
    st.pyplot(fig)
with scatter_col2:
    st.write("X2 vs Y")
    fig, ax = plt.subplots()
    sns.scatterplot(data=data, x='x2', y='y', ax=ax)
    st.pyplot(fig)

# Histogram
st.subheader("Histogram")
hist_col1, hist_col2 = st.columns(2)
with hist_col1:
    st.write("X1 distribution")
    fig, ax = plt.subplots()
    sns.histplot(data['x1'], bins=30, kde=True, ax=ax)
    st.pyplot(fig)
with hist_col2:
    st.write("X2 distribution")
    fig, ax = plt.subplots()
    sns.histplot(data['x2'], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

# Heatmap
st.subheader("Correlation Heatmap")
fig, ax = plt.subplots()
sns.heatmap(data.corr(), annot=True, cmap='coolwarm', ax=ax)
st.pyplot(fig)

# User feedback
st.header("User Feedback")
feedback = st.text_area("What do you think about this dashboard?", "")
if st.button("Submit Feedback"):
    st.write("Thank you for your feedback!")

# Footer
st.markdown("""
---
Built with ❤️ using [Streamlit](https://streamlit.io/).
""")