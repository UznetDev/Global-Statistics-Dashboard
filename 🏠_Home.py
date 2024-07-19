import streamlit as st
import altair as alt
import plotly.express as px
from loader import data, data_2023
from function import make_donut, write_stream_text, make_heatmap, abbreviate_number
from sklearn.preprocessing import MinMaxScaler



st.set_page_config(
    page_title="Global Statistics Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)


if st.sidebar.button("Predict NaN data", type="primary"):
    p_col = 'population'
    d_col = 'debt'
    g_col = 'GDP (current US$)'
else:
    p_col = 'Real Population'
    d_col = 'real debt'
    g_col = 'real GDP (current US$)'
    available_columns = [p_col, d_col, 'real GDP (current US$)']



alt.themes.enable("dark")


st.header('This is a Global Statistics Dashboard', divider='rainbow')
st.header('World economics and :blue[population] :sunglasses:')

text = "Global indicators of change in 2022 and 2023 in percentage"
st.write_stream(write_stream_text(text, 0.2))

d_2022 = data[data['Year'] == 2021][d_col].sum()
d_2023 = data[data['Year'] == 2023][d_col].sum()
d = round((d_2023 - d_2022) / d_2022 * 100, 2)

g_2022 = data[data['Year'] == 2021][g_col].sum()
g_2023 = data[data['Year'] == 2023][g_col].sum()
g = round((g_2023 - g_2022) / g_2022 * 100, 2)

p_2022 = data[data['Year'] == 2021][p_col].sum()
p_2023 = data[data['Year'] == 2023][p_col].sum()
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
    st.write(g_col)
    donut_chart_gdp = make_donut(g, g_col)
    st.altair_chart(donut_chart_gdp)



continent_population = data.groupby('continent')[p_col].sum().reset_index()
pie_df = data[data['Year'] == 2021].groupby('continent')[p_col].sum().reset_index()


pie_chart = px.pie(continent_population, 
                   names='continent', 
                   values=p_col, 
                   title=f'Population Share by Continent',
                   width=600, 
                   height=400)


histogram = px.histogram(pie_df,
                         x='continent', 
                         y=p_col, 
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

top_10_gdp_countries = data[data['Year'] == 2023].groupby('Country Name')[g_col].mean().reset_index().sort_values(g_col)


fig_top_10 = px.bar(top_10_gdp_countries.head(20), 
                    x='Country Name', 
                    y=g_col, 
                    title='Top 10 Countries by GDP (current US$)', 
                    labels={'Country Name': 'Country', g_col: g_col}, 
                    color=g_col,
                    color_continuous_scale=px.colors.sequential.YlOrRd)


if 'continent' in data.columns:
    fig_continent = px.histogram(data.sort_values(g_col), 
                                 x='continent', 
                                 y=g_col, 
                                 title='GDP (current US$) by Continent', 
                                 labels={'Continent': 'Continent', g_col: g_col}, 
                                 color='continent',
                                 color_discrete_sequence=px.colors.qualitative.Set3)
else:
    fig_continent = None

st.title('GDP Analysis')
cols = st.columns(2)
cols[0].plotly_chart(fig_top_10, use_container_width=True)



if fig_continent:
    cols[1].plotly_chart(fig_continent, use_container_width=True)
else:
    st.write("Data not found!")


st.warning('The average population, debt, and GDP (current US$) by year of the world.')
col =[p_col, d_col, g_col]
scaler = MinMaxScaler()
my_data = data.groupby('Year')[col].mean().reset_index()
my_data[col] = scaler.fit_transform(my_data[col])

fig = px.line(my_data, x="Year", y=my_data.columns, 
                    title=f"",
                    labels={"value": "Normalizations Value", "variable": "Indicator"})

st.plotly_chart(fig)

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
    st.write('Population by short region and year')
    my_data = data[(data['Year'] >= year_range[0]) & (data['Year'] <= year_range[1])]

    my_data['Short Population'] = my_data[p_col].agg(abbreviate_number)

    heatmap = make_heatmap(my_data, 'Year', 'sub_region', p_col, selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)



st.write('Dataframe')
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
col[1].write('Without Clening data')
col[0].write('With Clening data with predict')

cols = st.columns(2)



for i in range(0, len(pie_charts), 2):
    with cols[0]:
        
        st.plotly_chart(pie_charts[i], use_container_width=True)
    if i + 1 < len(pie_charts):
        with cols[1]:
            
            st.plotly_chart(pie_charts[i + 1], use_container_width=True)