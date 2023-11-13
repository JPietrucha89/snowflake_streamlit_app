import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

st.title('My Parents\' New Healthy Diner')
st.header('Breakfast Favorites')
st.text('🥣  Omega 3 & Blueberry Oatmeal')
st.text('🥗 Kale, Spinach & Rocket Smoothie')
st.text('🐔 Hard-Boiled Free-Range Egg')
st.text('🥑🍞 Avocado Toast')

st.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

### IMPORT CSV FROM WEB ###
# import CSV file from web in order to make df
my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# multiselect fruit picker with starting/default fruits. Store choice in variable list fruits_selected
fruits_selected = st.multiselect("Pick some fruits: ", list(my_fruit_list.Fruit), ['Avocado', 'Strawberries'])

# limit df only to fruits chosen in multiselect picker
fruits_to_show = my_fruit_list.loc[my_fruit_list.Fruit.isin(fruits_selected)]

# show df
st.dataframe(fruits_to_show)

st.header("Fruityvice Fruit Advice!")

### API CALL ###
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
st.stop() # temporarily stop execution of following code
my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * FROM fruit_load_list")
my_data_rows = my_cur.fetchall()

st.header("The fruit load list contains:")
st.dataframe(my_data_rows)

# allow user to add fruit to the list
add_my_fruit = st.text_input("Which fruit would you like to add?", "jackfruit")
st.write('Thanks for adding ', add_my_fruit)

# my_cur.execute("INSERT INTO fruit_load_list values (" & add_my_fruit & ")")
# my_cur.commit()
