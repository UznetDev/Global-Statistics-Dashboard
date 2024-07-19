import streamlit as st
import time
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from loader import data, pd
from function import abbreviate_number

st.set_page_config(
    page_title="Global Statistics Dashboard",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state="expanded"
)


st.title('Global Economic Indicators Dashboard')
my_data = data.copy()
my_data['debt'] = my_data['debt'].fillna(0)

column = st.selectbox('Qaysi ustun uchun bashorat qilishni xohlaysiz?', 
                      ['GDP (current US$)', 'population', 'debt'])
year = st.slider('Yilni tanlang', min_value=int(my_data['Year'].min()), max_value=int(my_data['Year'].max()) + 10, value=int(my_data['Year'].max()))
country = st.selectbox('Davlatni tanlang', my_data['Country Name'].unique())



features = [
    'Year', 
    'population', 
    # 'Density (P/Km2)', 
    # 'Land Area(Km2)', 
    # 'Latitude',
    # 'Longitude',
    'debt']

X = my_data[features]
y = my_data['GDP (current US$)']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)


y_pred = model.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
st.write(f"Mean Squared Error: {mse}")
st.write(f"R^2 Score: {r2}")



def stream_data():
    text = f"{country} da {year} yil uchun {column} predict qilib kuramiz, \n"
    for word in text.split(" "):
        yield word + " "
        time.sleep(0.02)


    re = my_data[(my_data['Country Name'] == country) & my_data[column] != 0][column]
    if not re.empty:
        re_dat = data[data['Country Name'] == country].sort_values(by='Year')
        re_dat['Previous Year Value'] = re_dat[column].shift(1)
        re_dat = re_dat.tail(5)

        re_dat['Growth Rate (%)'] = ((re_dat[column] - re_dat['Previous Year Value']) / re_dat['Previous Year Value']) * 100

        re_dat = re_dat.dropna(subset=['Growth Rate (%)'])
        text = '\nOxirgi 5 Yillik O\'sish Foizi\n'
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.02)
        st.write(re_dat[['Year', column, 'Growth Rate (%)']])
        # st.write(re.count())
        if re.count() < 53:
            text = "\nThe information is a bit sparse; this might reduce accuracy!\n"
            for word in text.split(" "):
                yield word + " "
                time.sleep(0.02)

        country_data = data[data['Country Name'] == country].iloc[0]
        input_data = {
            'Year': year,
            'population': country_data['population'],
            # 'Density (P/Km2)': country_data['Density (P/Km2)'],
            # 'Land Area(Km2)': country_data['Land Area(Km2)'],
            # 'Latitude': country_data['Latitude'],
            # 'Longitude': country_data['Longitude'],
            'debt': country_data['debt']
            
            }
        
        input_df = pd.DataFrame([input_data])
        predicted_value = model.predict(input_df[features])[0]

        actual_value = country_data[column]
        error_percentage = abs(predicted_value - actual_value) / actual_value

        text = f"\n{country} da {year}-yil uchun taxminan {column}:   {abbreviate_number(predicted_value)} \n"
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.02)
        text = f"\nAniqlig: {100 - error_percentage:.2f}% \n"
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.02)
        text = f"\nHaqiqiy {column}: {abbreviate_number(actual_value)} \n"
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.02)

    else:
        time.sleep(1)
        text = f'\nSorry, the information about {country} is very limited. Please choose another country!'
        for word in text.split(" "):
            yield word + " "
            time.sleep(0.02)


if st.button("Stream data"):
    st.write_stream(stream_data)


