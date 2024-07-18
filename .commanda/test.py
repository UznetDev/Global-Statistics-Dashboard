import streamlit as st
import plotly.express as px
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import seaborn as sns
import matplotlib.pyplot as plt
from loader import data_2023, data
from function import make_heatmap

color_theme_list = ['rainbow', 'blues', 'cividis', 'greens', 'inferno', 'magma', 'plasma', 'reds', 'turbo', 'viridis']

selected_color_theme = st.selectbox('Select a color theme', color_theme_list)
heatmap = make_heatmap(data, 'Year', 'continent', 'population', selected_color_theme)
st.altair_chart(heatmap, use_container_width=True)


