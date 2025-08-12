
import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium

st.set_page_config(page_title="Edinburgh Uni Accommodation Selector", layout="wide")

st.title("Edinburgh University Accommodation Selector")

# Load data
df = pd.read_csv("data/edinburgh_accommodation_enriched.csv")

# Filters
ensuite_filter = st.sidebar.selectbox("Ensuite", ["Any", "Yes", "No"])
max_rent = st.sidebar.slider("Max Weekly Rent (£)", 80, 250, 250)

filtered_df = df.copy()
if ensuite_filter != "Any":
    filtered_df = filtered_df[filtered_df["Ensuite"].str.lower() == ensuite_filter.lower()]
filtered_df = filtered_df[filtered_df["Weekly Rent (£)"] <= max_rent]

# Map
m = folium.Map(location=[55.944, -3.189], zoom_start=14)
for _, row in filtered_df.iterrows():
    popup_html = f"""
    <b>{row['Name']}</b><br>
    Ensuite: {row['Ensuite']}<br>
    Rent: £{row['Weekly Rent (£)']} / week<br>
    Walk to campus: {row['Walk to Campus (min)']} min<br>
    Walk to gym: {row['Walk to Gym (min)']} min<br>
    Walk to supermarket: {row['Walk to Supermarket (min)']} min<br>
    Walk to Old Town: {row['Walk to Old Town (min)']} min<br>
    Rating: {row['Rating']}/5<br>
    Ownership: {row['Ownership']}<br>
    <a href='{row['Official URL']}' target='_blank'>Official page</a>
    """
    folium.Marker(
        [row['Latitude'], row['Longitude']],
        popup=folium.Popup(popup_html, max_width=300)
    ).add_to(m)

st_data = st_folium(m, width=900, height=600)

st.subheader("Accommodation List")
st.dataframe(filtered_df)
