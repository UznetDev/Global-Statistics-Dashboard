import streamlit as st
import folium
from streamlit_folium import folium_static
from loader import data, pd
import plotly.express as px
from sklearn.preprocessing import MinMaxScaler
from function import abbreviate_number



st.set_page_config(
    page_title="Global Statistics Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.header('This is a Global Statistics Map for population by year', divider='rainbow')

st.sidebar.title("Select Year")
year = st.sidebar.selectbox("Year", data['Year'].unique())


filtered_data = data[data['Year'] == year]


filtered_data = filtered_data.dropna(subset=['Latitude', 'Longitude'])


map = folium.Map(location=[20, 0], zoom_start=2)

for _, row in filtered_data.iterrows():
    popup_text = f"""
    <b>Country: {row['Country Name']}<br>
    Debt: {abbreviate_number(row['debt']) if not pd.isna(row['debt']) else 'Data not found'}<br>
    Population: {abbreviate_number(row['population']) if not pd.isna(row['population']) else 'Data not found'}<br>
    GDP: {abbreviate_number(row['GDP (current US$)']) if not pd.isna(row['GDP (current US$)']) else 'Data not found'}<br>
    Density (P/Km2): {row['Density (P/Km2)'] if not pd.isna(row['Density (P/Km2)']) else 'Data not found'}<br>
    Land Area(Km2): {row['Land Area(Km2)'] if not pd.isna(row['Land Area(Km2)']) else 'Data not found'}<br>
</b>
    """
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup_text
    ).add_to(map)

folium_static(map)
st.warning('The average population, debt, and GDP (current US$) by year of the world.')
col =['population', 'debt', 'GDP (current US$)']
scaler = MinMaxScaler()
my_data = data.groupby('Year')[col].mean().reset_index()
my_data[col] = scaler.fit_transform(my_data[col])

fig = px.line(my_data, x="Year", y=my_data.columns, 
                    title=f"",
                    labels={"value": "Normalizations Value", "variable": "Indicator"})

st.plotly_chart(fig)