import streamlit as st
import altair as alt
import plotly.express as px
from loader import data, data_2023
from function import make_donut, wrete_stream_text, make_heatmap, abbreviate_number


st.set_page_config(
    page_title="Global Statistics Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)

alt.themes.enable("dark")


st.header('This is a Global Statistics Dashboard', divider='rainbow')
st.header('World economics and :blue[population] :sunglasses:')

text = "Dunyo buyicha 2022 yil va 2023 yil uzgarish kursatgichi foizda"
st.write_stream(wrete_stream_text(text, 0.2))

d_2022 = data[data['Year'] == 2021]['debt'].sum()
d_2023 = data[data['Year'] == 2023]['debt'].sum()
d = round((d_2023 - d_2022) / d_2022 * 100, 2)

g_2022 = data[data['Year'] == 2021]['GDP (current US$)'].sum()
g_2023 = data[data['Year'] == 2023]['GDP (current US$)'].sum()
g = round((g_2023 - g_2022) / g_2022 * 100, 2)

p_2022 = data[data['Year'] == 2021]['population'].sum()
p_2023 = data[data['Year'] == 2023]['population'].sum()
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


continent_population = data.groupby('continent')['population'].sum().reset_index()
pie_df = data[data['Year'] == 2021].groupby('continent')['population'].sum().reset_index()


pie_chart = px.pie(continent_population, 
                   names='continent', 
                   values='population', 
                   title='Population Share by Continent',
                   width=600, 
                   height=400)


histogram = px.histogram(pie_df,
                         x='continent', 
                         y='population', 
                         histfunc='avg', 
                         title='Average Population by Continent in 2021',
                         width=800, 
                         height=400,
                         color='continent',
                         color_discrete_sequence=px.colors.qualitative.Set3)


text = "Populatsion buyicha mintaqa va davlatlar reytingi va ulushi."
st.write_stream(wrete_stream_text(text, 0.2))

col1, col2 = st.columns(2, gap='small')

df_selected_year_sorted = data_2023.sort_values('Population', ascending=False)[['Population', 'Country']]

with col1:
    st.plotly_chart(pie_chart, theme=None)

with col2:
    st.plotly_chart(histogram, theme=None)

col1, col2 = st.columns(2, gap='small')

with col1:
    st.markdown('#### Top Country')
    st.dataframe(
        df_selected_year_sorted,
        column_order=["Country", "Population"],
        hide_index=True,
        column_config={
            "Country": st.column_config.TextColumn(
                "Country",
            ),
            "Population": st.column_config.ProgressColumn(
                "Population",
                format="%f",
                min_value=0,
                max_value=max(df_selected_year_sorted['Population']),
            )
        },
        width=350
    )
with col2:
    color_theme_list = ['rainbow', 'blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
    year_min = 1970
    year_max = 2023
    year_range = st.slider("Select Year Range for headmap", min_value=year_min, max_value=year_max, value=(2010, year_max))

    my_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]

    my_data['Short Population'] = my_data['population'].agg(abbreviate_number)

    heatmap = make_heatmap(my_data, 'Year', 'sub_region', 'population', selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)
