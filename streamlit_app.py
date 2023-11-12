import streamlit as st
import pandas as pd
import requests

st.title('My Parents\' New Healthy Diner')
st.header('Breakfast Favorites')
st.text('🥣  Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# import CSV file from web in order to make df
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# multiselect fruit picker with starting/default fruits. Store choice in variable list fruits_selected
fruits_selected = st.multiselect("Pick some fruits: ", list(my_fruit_list.Fruit), ['Avocado', 'Strawberries'])

# limit df only to fruits chosen in multiselect picker
fruits_to_show = my_fruit_list.loc[my_fruit_list.Fruit.isin(fruits_selected)]

# show df
st.dataframe(fruits_to_show)

# Request to Fruityvice API
chosen_fruit = 'kiwi'
fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{chosen_fruit}")

st.header("Fruityvice Fruit Advice!")

# get text from response object and normalize returned json
fruityvice_response_json = fruityvice_response.json()
fruityvice_normalized = pd.json_normalize(fruityvice_response_json)

# print normalized json as table
st.dataframe(fruityvice_normalized)
