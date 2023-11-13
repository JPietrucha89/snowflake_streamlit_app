import streamlit as st
import pandas as pd
import requests
import snowflake.connector

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

st.header("Fruityvice Fruit Advice!")

# Request to Fruityvice API
fruit_choice = st.text_input('What fruit would you like information about?', 'Apple')
st.write('User entered:', fruit_choice)

fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_choice}")

# get text from response object and normalize returned json
fruityvice_response_json = fruityvice_response.json()
fruityvice_normalized = pd.json_normalize(fruityvice_response_json)

# print normalized json as table
st.dataframe(fruityvice_normalized)

### CONNECTING TO SNOWFLAKE #####
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.exectue("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION();")
my_data_row = my_cur.fetchone()

st.text("Hello from Snowflake:")
st.text(my_data_row)