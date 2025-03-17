import streamlit as st
import pandas as pd

# Title of the app
st.title("IMDB Top 250 Movies Data")

# Load some data
data = pd.read_csv("top_250_movies.csv")
data[["Rating","Count"]] = data['Rating'].str.extract(r'(\d+\.?\d*)\((.*?)\)')
data["Rating"] = data["Rating"].astype(float)

# Display the DataFrame
st.write("Here's the dataset:")
st.write(data)

# Add a slider to filter by age
rating_filter = st.slider("Filter by Rating", min_value=0, max_value=10, value=(0, 10))

# Filter the data based on the slider
filtered_data = data[(data["Rating"] >= rating_filter[0]) & (data["Rating"] <= rating_filter[1])]

# Display the filtered data
st.write("Filtered Data:")
st.write(filtered_data)
