import streamlit as st
import altair as alt
import plotly.express as px
from loader import data, data_2023
from function import make_donut, write_stream_text, make_heatmap, abbreviate_number


st.set_page_config(
    page_title="Global Statistics Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)


if st.button("Predict NaN data", type="primary"):
    p_col = 'population'
    d_col = 'debt'
    g_col = 'GDP (current US$'
else:
    p_col = 'Real population'
    d_col = 'real debt'
    g_col = 'real GDP (current US$'
    available_columns = ['Real Population', 'real debt', 'real GDP (current US$)']



alt.themes.enable("dark")


st.header('This is a Global Statistics Dashboard', divider='rainbow')
st.header('World economics and :blue[population] :sunglasses:')

text = "Global indicators of change in 2022 and 2023 in percentage"
st.write_stream(write_stream_text(text, 0.2))

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





text = "Regional and country population rankings and shares."
st.write_stream(write_stream_text(text, 0.2))

col1, col2 = st.columns(2, gap='small')

df_selected_year_sorted = data_2023.sort_values('Population', ascending=False)[['Population', 'Country']]

with col1:
    st.plotly_chart(pie_chart, theme=None)

with col2:
    st.plotly_chart(histogram, theme=None)


#-----------------------------------------------------------------------------------------------------

top_10_gdp_countries = data[data['Year'] == 2023].groupby('Country Name')['GDP (current US$)'].mean().reset_index().sort_values('GDP (current US$)')


fig_top_10 = px.bar(top_10_gdp_countries.head(20), 
                    x='Country Name', 
                    y='GDP (current US$)', 
                    title='Top 10 Countries by GDP (current US$)', 
                    labels={'Country Name': 'Country', 'GDP (current US$)': 'GDP (current US$)'}, 
                    color='GDP (current US$)',
                    color_continuous_scale=px.colors.sequential.YlOrRd)


if 'continent' in data.columns:
    fig_continent = px.histogram(data.sort_values('GDP (current US$)'), 
                                 x='continent', 
                                 y='GDP (current US$)', 
                                 title='GDP (current US$) by Continent', 
                                 labels={'Continent': 'Continent', 'GDP (current US$)': 'GDP (current US$)'}, 
                                 color='continent',
                                 color_discrete_sequence=px.colors.qualitative.Set3)
else:
    fig_continent = None

st.title('GDP Analysis')
cols = st.columns(2)
cols[0].plotly_chart(fig_top_10, use_container_width=True)

year_min = 1970
year_max = 2023
year_range = cols[0].slider("Select Year Range", min_value=year_min, max_value=year_max, value=(year_min, year_max))


if fig_continent:
    cols[1].plotly_chart(fig_continent, use_container_width=True)
else:
    st.write("Data not found!")

#-------------------------------------------------------------------------------------------------


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




st.dataframe(data.head())



columns_to_check = ["GDP (current US$)", "real GDP (current US$)", 
                    "population", "Real Population", 
                    "debt", "real debt"]

color_discrete_map = {
    "Data Exist": "blue",
    "No Data": "red"
}

pie_charts = []


for column in columns_to_check:
    col_data = data[column].isna()
    counts = col_data.value_counts().reset_index()
    counts.columns = ['data_exists', 'count']
    counts['data_exists'] = counts['data_exists'].map({False: 'Data Exist', True: 'No Data'})

    pie_chart = px.pie(counts, 
                       names='data_exists', 
                       values='count', 
                       title=column,
                       color='data_exists',
                       color_discrete_map=color_discrete_map,
                       width=400, 
                       height=400)
    pie_charts.append(pie_chart)




st.title('Data Missing Analysis')

col = st.columns(2)
col[0].write('Without Clening data')
col[1].write('With Clening data')

cols = st.columns(2)



for i in range(0, len(pie_charts), 2):
    with cols[0]:
        
        st.plotly_chart(pie_charts[i], use_container_width=True)
    if i + 1 < len(pie_charts):
        with cols[1]:
            
            st.plotly_chart(pie_charts[i + 1], use_container_width=True)