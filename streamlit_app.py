import streamlit as st
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

def get_fruityvice_data(this_fruit_choice):
  # Request to Fruityvice API
  fruityvice_response = requests.get(f"https://fruityvice.com/api/fruit/{this_fruit_choice}")
  # get text from response object and normalize returned json
  fruityvice_response_json = fruityvice_response.json()
  fruityvice_normalized = pd.json_normalize(fruityvice_response_json)
  return fruityvice_normalized
  
### MAIN ###
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

### API CALL ###
st.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = st.text_input('What fruit would you like information about?')
  if not fruit_choice:
    st.error("Please select a fruit to get information.")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    # print normalized json as table
    st.dataframe(back_from_function)
except URLError as e:
  st.error()
  
### CONNECTING TO SNOWFLAKE #####
st.header("The fruit load list contains:")

def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("SELECT * FROM fruit_load_list")
    return my_cur.fetchall()

if st.button("Get Fruit Load List"):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  st.dataframe(my_data_rows)

# allow user to add fruit to the list
def check_if_fruit_exists_in_snowflake_table(new_fruit):
  with my_cnx.cursor() as my_cur: 
    my_cur.execute( "select count(*) from fruit_load_list where fruit_name = '" + new_fruit + "' )" )
    count_of_new_fruit_in_table = cast(my_cur.fetchone() as number)
    if count_of_new_fruit_in_table > 0: 
      result = False 
    else: 
      result = True
    return result
    
def insert_row_to_snowflake_table(new_fruit):
  with my_cnx.cursor() as my_cur:
    #if check_if_fruit_exists_in_snowflake_table(new_fruit) == False:
     my_cur.execute( "INSERT INTO fruit_load_list values ('" + new_fruit + "')" )
       #my_cur.commit()
     return f"Thanks for adding {new_fruit}"
    #else:
      #return f"{new_fruit} already exists in table!"
      
add_my_fruit = st.text_input("Which fruit would you like to add?", "jackfruit")
if st.button("Add a Fruit to the List"):
  my_cnx = snowflake.connector.connect(**st.secrets["snowflake"])
  back_from_function = insert_row_to_snowflake_table(add_my_fruit)
  
st.stop() # temporarily stop execution of following code


