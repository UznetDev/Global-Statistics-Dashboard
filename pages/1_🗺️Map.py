import streamlit as st
import folium
from streamlit_folium import folium_static
from loader import data, pd

st.set_page_config(
    page_title="Global Statistics Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.header('This is a Global Statistics Map', divider='rainbow')

st.sidebar.title("Select Year")
year = st.sidebar.selectbox("Year", data['Year'].unique())


filtered_data = data[data['Year'] == year]


filtered_data = filtered_data.dropna(subset=['Latitude', 'Longitude'])


map = folium.Map(location=[20, 0], zoom_start=2)

for _, row in filtered_data.iterrows():
    popup_text = f"""
    <b>Country: {row['Country Name']}<br>
    Debt: {row['debt'] if not pd.isna(row['debt']) else 'Data not found'}<br>
    Population: {row['population'] if not pd.isna(row['population']) else 'Data not found'}<br>
    GDP: {row['GDP (current US$)'] if not pd.isna(row['GDP (current US$)']) else 'Data not found'}<br>
    Density (P/Km2): {row['Density (P/Km2)'] if not pd.isna(row['Density (P/Km2)']) else 'Data not found'}<br>
    Land Area(Km2): {row['Land Area(Km2)'] if not pd.isna(row['Land Area(Km2)']) else 'Data not found'}<br>
</b>
    """
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup_text
    ).add_to(map)

folium_static(map)