import streamlit as st
import numpy as np
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


if st.button("Predict NaN data", type="primary"):
    available_columns = ['population', 'debt', 'GDP (current US$)']
else:
    available_columns = ['Real Population', 'real debt', 'real GDP (current US$)']

re_col = None

columns = st.sidebar.multiselect("Select Columns to Display", options=available_columns, default=[re_col if re_col else available_columns[0]])

re_col = columns

year_min = 1970
year_max = 2023
year_range = st.sidebar.slider("Select Year Range", min_value=year_min, max_value=year_max, value=(year_min, year_max))


country_data = data[(data['Country Name'] == country) & (data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])].copy()
country_data_copy = country_data.copy()


for c in columns:
    country_data[c] = country_data[c].apply(lambda x: np.nan if x == 0 else x)

if st.button("Drop NaN"):
    country_data.dropna(subset=columns, inplace=True)
    for c in columns:
        country_data_copy[c] = country_data_copy[c].apply(lambda x: np.nan if x == 0 else x)
    country_data_copy.dropna(subset=columns, inplace=True)
    


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


if columns:
    col = st.columns(len(columns))
    for i in range(len(columns)):
        c = columns[i]
        country_data_copy[c+'_group'] = country_data_copy[c].apply(lambda x: 'No Data' if x == 0 else 'Exist Data')
        counts = country_data_copy[c+'_group'].value_counts().reset_index()
        counts.columns = ['Status', 'Count']
        pie_chart = px.pie(counts, 
                        names='Status', 
                        values='Count', 
                        title=f'{c} missing data!',
                        width=600, 
                        height=400)
        col[i].plotly_chart(pie_chart, theme=None)







if not existing_columns:
    st.error("Selected columns are not available in the 2023 data.")
else:

    scaler = MinMaxScaler()
    existing_daat = country_data.copy()
    existing_daat[existing_columns] = scaler.fit_transform(existing_daat[existing_columns])


    fig = px.line(existing_daat, x="Year", y=columns, 
                  title=f"{', '.join(columns).title()} Over Years for {country} ({year_range[0]}-{year_range[1]})",
                  labels={"value": "Normalizations Value", "variable": "Indicator"})


    st.plotly_chart(fig)

    col = st.columns(len(columns))

    for i in range(len(columns)):
        with col[i]:
            fig = px.line(country_data[['Year', columns[i]]], x="Year", y=columns[i], 
                    title=f"{columns[i].title()} Over Years for {country} ({year_range[0]}-{year_range[1]})",
                    labels={"value": "Value", "variable": "Indicator"})
            st.plotly_chart(fig)


    col = st.columns(len(columns))

    for i in range(len(columns)):
        histogram = px.histogram(country_data,
                        x='Year', 
                        y=columns[i], 
                        histfunc='avg', 
                        title='Average Population by Continent in 2021',
                        width=800, 
                        height=400,
                        color=columns[i],
                        color_discrete_sequence=px.colors.qualitative.Set3)
        col[i].plotly_chart(histogram, theme=None)
            
    last_country_data = data_2023[data_2023['Country'] == country]

    last_num_data = last_country_data.select_dtypes('number')
    n_cols = [
            'Agricultural Land( %)', 
            'Armed Forces size', 
            'Birth Rate',
            'CPI',
            'Gross primary education enrollment (%)',
            'Gross tertiary education enrollment (%)',
            'Life expectancy',
            'Physicians per thousand',
            'Unemployment rate',
            'Urban_population',
            'Forested Area (%)'
            ]

    ln = len(n_cols)
    cols1 = st.columns(ln)
    cols2 = st.columns(ln)



    for i in range(1, ln, 2):
        col = n_cols[i]
        rotated_text = f"""
    <div style="transform: rotate(45deg); white-space: nowrap;">
        {col}
    </div>
    """
        cols1[i].write(rotated_text, unsafe_allow_html=True)
        re = round(((data_2023[col].mean() - last_num_data[col]) / last_num_data[col]) * 100, 2)
        cols1[i].metric('', last_num_data[col].mean(), f"{float(re)} %")
        

        col2 = n_cols[i-1]
        rotated_text = f"""
    <div style="transform: rotate(45deg); white-space: nowrap;">
        {col2}
    </div>
    """
        cols2[i].write(rotated_text, unsafe_allow_html=True)
        re2 = round(((data_2023[col].mean() - last_num_data[col2]) / last_num_data[col2]) * 100, 2)
        cols2[i].metric('', last_num_data[col2].mean(), f"{float(re2)} %")
        
        

    text = f"{country}\n"
    for column in last_country_data.columns:
        value = last_country_data[column].values[0]
        text = f"{column}:      {value}\n"
        st.write_stream(write_stream_text(text))