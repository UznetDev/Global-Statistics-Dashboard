# import streamlit as st
# import pandas as pd
# import time
# import matplotlib.pyplot as plt
# import seaborn as sns


# st.write("# My First App")

# st.write("## Second Header")

# df = pd.read_csv("ds_salaries_clean.csv")
# st.write(df.head())


# # st.line_chart(df["Salary_USD"])

# # bin = st.select_slider(
# #     "select bin number",
# #     options=list(range(1, 26)))
# # st.write("My favorite color is", bin)
# # fig, ax = plt.subplots()
# # sns.histplot(df['Salary_USD'], bins=bin, ax=ax)
# # st.pyplot(fig)


# # genre = st.radio(
# #     label = "Tajriba Darajasini Tanlang",
# #     options = df['Company_Size'].unique().tolist(),
# #     index=None,
# # )
# # if st.button("Jadvalni Ko'rsat"):
# #     # st.write("Why hello there")
# #     # st.write("You selected:", genre)

# #     st.dataframe(df[df["Company_Size"]==genre])
# # else:
# #     pass
# st.write("area_chart")
# st.area_chart(df["Salary_USD"])
# st.write(df["Salary_USD"].max())

# st.write("barchart")
# st.bar_chart(df["Salary_USD"])


# st.write("barchart")






# with st.sidebar:

#     st.line_chart(df["Salary_USD"])

#     with st.echo():
#         st.write("This code will be printed to the sidebar.")

#     with st.spinner("Loading..."):
#         time.sleep(5)
#     st.success("Done!")





# tab1, tab2, tab3 = st.tabs(["Mushuk", "Kuchuk", "Boyo'gli (Boyqush)"])

# with tab1:
#    st.header("A cat")
#    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

#    st.line_chart(df["Salary_USD"])

# with tab2:
#    st.header("A dog")
#    st.image("https://static.streamlit.io/examples/dog.jpg", width=200)

# with tab3:
#    st.header("An owl")
#    st.image("https://static.streamlit.io/examples/owl.jpg", width=200)



#######################
# Import libraries
import streamlit as st
import pandas as pd
import altair as alt
import plotly.express as px

#######################
# Page configuration
st.set_page_config(
    page_title="US Population Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded")

alt.themes.enable("dark")


#######################
# Load data
df_reshaped = pd.read_csv('dataset/us-population-2010-2019-reshaped.csv')


#######################
# Sidebar
with st.sidebar:
    st.title('🏂 US Population Dashboard')

    year_list = list(df_reshaped.year.unique())[::-1]

    selected_year = st.selectbox('Select a year', year_list)
    df_selected_year = df_reshaped[df_reshaped.year == selected_year]
    df_selected_year_sorted = df_selected_year.sort_values(by="population", ascending=False)

    color_theme_list = ['blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'rainbow', 'turbo', 'viridis']
    selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


#######################
# Plots

# Heatmap
def make_heatmap(input_df, input_y, input_x, input_color, input_color_theme):
    heatmap = alt.Chart(input_df).mark_rect().encode(
            y=alt.Y(f'{input_y}:O', axis=alt.Axis(title="Year", titleFontSize=18, titlePadding=15, titleFontWeight=900, labelAngle=0)),
            x=alt.X(f'{input_x}:O', axis=alt.Axis(title="", titleFontSize=18, titlePadding=15, titleFontWeight=900)),
            color=alt.Color(f'max({input_color}):Q',
                             legend=None,
                             scale=alt.Scale(scheme=input_color_theme)),
            stroke=alt.value('black'),
            strokeWidth=alt.value(0.25),
        ).properties(width=900
        ).configure_axis(
        labelFontSize=12,
        titleFontSize=12
        )
    # height=300
    return heatmap

# Choropleth map
def make_choropleth(input_df, input_id, input_column, input_color_theme):
    choropleth = px.choropleth(input_df, locations=input_id, color=input_column, locationmode="USA-states",
                               color_continuous_scale=input_color_theme,
                               range_color=(0, max(df_selected_year.population)),
                               scope="usa",
                               labels={'population':'Population'}
                              )
    choropleth.update_layout(
        template='plotly_dark',
        plot_bgcolor='rgba(0, 0, 0, 0)',
        paper_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(l=0, r=0, t=0, b=0),
        height=350
    )
    return choropleth


# Donut chart
def make_donut(input_response, input_text, input_color):
  if input_color == 'blue':
      chart_color = ['#29b5e8', '#155F7A']
  if input_color == 'green':
      chart_color = ['#27AE60', '#12783D']
  if input_color == 'orange':
      chart_color = ['#F39C12', '#875A12']
  if input_color == 'red':
      chart_color = ['#E74C3C', '#781F16']

  source = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100-input_response, input_response]
  })
  source_bg = pd.DataFrame({
      "Topic": ['', input_text],
      "% value": [100, 0]
  })

  plot = alt.Chart(source).mark_arc(innerRadius=45, cornerRadius=25).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          #domain=['A', 'B'],
                          domain=[input_text, ''],
                          # range=['#29b5e8', '#155F7A']),  # 31333F
                          range=chart_color),
                      legend=None),
  ).properties(width=130, height=130)

  text = plot.mark_text(align='center', color="#29b5e8", font="Lato", fontSize=32, fontWeight=700, fontStyle="italic").encode(text=alt.value(f'{input_response} %'))
  plot_bg = alt.Chart(source_bg).mark_arc(innerRadius=45, cornerRadius=20).encode(
      theta="% value",
      color= alt.Color("Topic:N",
                      scale=alt.Scale(
                          # domain=['A', 'B'],
                          domain=[input_text, ''],
                          range=chart_color),  # 31333F
                      legend=None),
  ).properties(width=130, height=130)
  return plot_bg + plot + text

# Convert population to text
def format_number(num):
    if num > 1000000:
        if not num % 1000000:
            return f'{num // 1000000} M'
        return f'{round(num / 1000000, 1)} M'
    return f'{num // 1000} K'

# Calculation year-over-year population migrations
def calculate_population_difference(input_df, input_year):
  selected_year_data = input_df[input_df['year'] == input_year].reset_index()
  previous_year_data = input_df[input_df['year'] == input_year - 1].reset_index()
  selected_year_data['population_difference'] = selected_year_data.population.sub(previous_year_data.population, fill_value=0)
  return pd.concat([selected_year_data.states, selected_year_data.id, selected_year_data.population, selected_year_data.population_difference], axis=1).sort_values(by="population_difference", ascending=False)


#######################
# Dashboard Main Panel
col = st.columns((1.5, 4.5, 2), gap='medium')

with col[0]:
    st.markdown('#### Gains/Losses')

    df_population_difference_sorted = calculate_population_difference(df_reshaped, selected_year)

    if selected_year > 2010:
        first_state_name = df_population_difference_sorted.states.iloc[0]
        first_state_population = format_number(df_population_difference_sorted.population.iloc[0])
        first_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[0])
    else:
        first_state_name = '-'
        first_state_population = '-'
        first_state_delta = ''
    st.metric(label=first_state_name, value=first_state_population, delta=first_state_delta)

    if selected_year > 2010:
        last_state_name = df_population_difference_sorted.states.iloc[-1]
        last_state_population = format_number(df_population_difference_sorted.population.iloc[-1])
        last_state_delta = format_number(df_population_difference_sorted.population_difference.iloc[-1])
    else:
        last_state_name = '-'
        last_state_population = '-'
        last_state_delta = ''
    st.metric(label=last_state_name, value=last_state_population, delta=last_state_delta)


    st.markdown('#### States Migration')

    if selected_year > 2010:
        
        df_greater_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference > 50000]
        df_less_50000 = df_population_difference_sorted[df_population_difference_sorted.population_difference < -50000]

        # % of States with population difference > 50000
        states_migration_greater = round((len(df_greater_50000)/df_population_difference_sorted.states.nunique())*100)
        states_migration_less = round((len(df_less_50000)/df_population_difference_sorted.states.nunique())*100)
        donut_chart_greater = make_donut(states_migration_greater, 'Inbound Migration', 'green')
        donut_chart_less = make_donut(states_migration_less, 'Outbound Migration', 'red')
    else:
        states_migration_greater = 0
        states_migration_less = 0
        donut_chart_greater = make_donut(states_migration_greater, 'Inbound Migration', 'green')
        donut_chart_less = make_donut(states_migration_less, 'Outbound Migration', 'red')

    migrations_col = st.columns((0.2, 1, 0.2))
    with migrations_col[1]:
        st.write('Inbound')
        st.altair_chart(donut_chart_greater)
        st.write('Outbound')
        st.altair_chart(donut_chart_less)

with col[1]:
    st.markdown('#### Total Population')

    choropleth = make_choropleth(df_selected_year, 'states_code', 'population', selected_color_theme)
    st.plotly_chart(choropleth, use_container_width=True)

    heatmap = make_heatmap(df_reshaped, 'year', 'states', 'population', selected_color_theme)
    st.altair_chart(heatmap, use_container_width=True)


with col[2]:
    st.markdown('#### Top States')

    st.dataframe(df_selected_year_sorted,
                 column_order=("states", "population"),
                 hide_index=True,
                 width=None,
                 column_config={
                    "states": st.column_config.TextColumn(
                        "States",
                    ),
                    "population": st.column_config.ProgressColumn(
                        "Population",
                        format="%f",
                        min_value=0,
                        max_value=max(df_selected_year_sorted.population),
                     )}
                 )

    with st.expander('About', expanded=True):
        st.write('''
            - Data: [U.S. Census Bureau](https://www.census.gov/data/datasets/time-series/demo/popest/2010s-state-total.html).
            - :orange[**Gains/Losses**]: states with high inbound/ outbound migration for selected year
            - :orange[**States Migration**]: percentage of states with annual inbound/ outbound migration > 50,000
            ''')



import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from loader import data

# Ma'lumotlarni tozalash
df['Density (P/Km2)'] = pd.to_numeric(df['Density (P/Km2)'].str.replace(',', '.'), errors='coerce')
df['Land Area(Km2)'] = pd.to_numeric(df['Land Area(Km2)'].str.replace(',', ''), errors='coerce')
df.dropna(subset=[])
df['Density (P/Km2)'].fillna(df['Density (P/Km2)'].mean(), inplace=True)
df['Land Area(Km2)'].fillna(df['Land Area(Km2)'].mean(), inplace=True)
df['Latitude'].fillna(df['Latitude'].mean(), inplace=True)
df['Longitude'].fillna(df['Longitude'].mean(), inplace=True)
df['GDP (current US$)'].fillna(df['GDP (current US$)'].mean(), inplace=True)
df['population'].fillna(df['population'].mean(), inplace=True)
data['debt'].fillna(data['debt'].mean(), inplace=True)



st.title('Mamlakatlar iqtisodiy ko\'rsatkichlari dashboardi')




st.subheader('YAIM (GDP) bashorati')


features = ['Year', 'population', 'Density (P/Km2)', 'Land Area(Km2)', 'Latitude', 'Longitude', 'debt']
X = data[features]
y = data['GDP (current US$)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)


mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
st.write(f"Mean Squared Error: {mse}")
st.write(f"R^2 Score: {r2}")


result = pd.DataFrame({'Haqiqiy YAIM': y_test, 'Bashorat qilingan YAIM': y_pred})
st.write(result.head())


st.subheader('Aniq davlat va yil uchun YAIM bashorati')
country = st.selectbox('Davlatni tanlang', data['Country Name'].unique())
year = st.slider('Yilni tanlang', min_value=int(data['Year'].min()), max_value=int(data['Year'].max()) + 30, value=int(data['Year'].max()))


column = st.selectbox('Qaysi ustun uchun bashorat qilish kerak?', ['GDP (current US$)', 'population', 'debt'])

if st.button('Bashorat qilish'):
    country_data = data[data['Country Name'] == country].iloc[0]
    input_data = {
        'Year': year,
        'population': country_data['population'],
        'Density (P/Km2)': country_data['Density (P/Km2)'],
        'Land Area(Km2)': country_data['Land Area(Km2)'],
        'Latitude': country_data['Latitude'],
        'Longitude': country_data['Longitude'],
        'debt': country_data['debt']
    }

    input_df = pd.DataFrame([input_data])
    predicted_value = model.predict(input_df[features])[0]

    actual_value = country_data[column]
    error_percentage = abs(predicted_value - actual_value) / actual_value * 100

    st.write(f"{country} davlatining {year}-yil uchun bashorat qilingan {column}: ${predicted_value:,.2f}")
    st.write(f"Haqiqiy {column}: ${actual_value:,.2f}")
    st.write(f"Bashorat aniqligi: {100 - error_percentage:.2f}%")



import time
import numpy as np
import pandas as pd
import streamlit as st

_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""


def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)


if st.button("Stream data"):
    st.write_stream(stream_data)