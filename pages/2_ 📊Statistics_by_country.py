import streamlit as st
import plotly.express as px
from loader import data, data_2023
from function import make_donut, write_stream_text
from sklearn.preprocessing import MinMaxScaler


st.set_page_config(
    page_title="Global Statistics Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)


country = st.sidebar.selectbox("Select Country", data['Country Name'].unique())
st.header(f'Statistics Dashboard for {country}', divider='rainbow')

available_columns = ['population', 'debt', 'GDP (current US$)']
columns = st.sidebar.multiselect("Select Columns to Display", options=available_columns, default=['population'])


year_min = 1970
year_max = 2023
year_range = st.sidebar.slider("Select Year Range", min_value=year_min, max_value=year_max, value=(year_min, year_max))


country_data = data[(data['Country Name'] == country) & (data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]


existing_columns = [col for col in columns if col in data.columns]



d_2022 = country_data[country_data['Year'] == year_min]['debt'].sum()
d_2023 = country_data[country_data['Year'] == year_max]['debt'].sum()
d = round((d_2023 - d_2022) / d_2022 * 100, 2)

g_2022 = country_data[country_data['Year'] == year_min]['GDP (current US$)'].sum()
g_2023 = country_data[country_data['Year'] == year_max]['GDP (current US$)'].sum()
g = round((g_2023 - g_2022) / g_2022 * 100, 2)

p_2022 = country_data[country_data['Year'] == year_min]['population'].sum()
p_2023 = country_data[country_data['Year'] == year_max]['population'].sum()
p = round((p_2023 - p_2022) / p_2022 * 100, 2)


col1, col2, col3 = st.columns(3)



with col1:
    st.write('Population raise')
    donut_chart_population = make_donut(p, 'Population raise')
    st.altair_chart(donut_chart_population)

with col2:  
    st.write('Debt change')
    donut_chart_debt = make_donut(d, 'Debt change')
    st.altair_chart(donut_chart_debt)

with col3:
    st.write('GDP (current US$)')
    donut_chart_gdp = make_donut(g, 'GDP (current US$)')
    st.altair_chart(donut_chart_gdp)



if not existing_columns:
    st.error("Selected columns are not available in the 2023 data.")
else:

    scaler = MinMaxScaler()
    country_data[existing_columns] = scaler.fit_transform(country_data[existing_columns])


    fig = px.line(country_data, x="Year", y=columns, 
                  title=f"{', '.join(columns).title()} Over Years for {country} ({year_range[0]}-{year_range[1]})",
                  labels={"value": "Normalizations Value", "variable": "Indicator"})


    st.plotly_chart(fig)


    
last_country_data = data_2023[data_2023['Country'] == country]
text = f"{country}\n"
for column in last_country_data.columns:
    value = last_country_data[column].values[0]
    text = f"{column}:      {value}\n"
    st.write_stream(write_stream_text(text))