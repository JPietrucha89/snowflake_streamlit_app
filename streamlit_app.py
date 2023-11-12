import streamlit as st
import pandas as pd

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
fruits_selected = st.multiselect("Pick some fruits: ", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

# limit df only to fruits chosen in multiselect picker
fruits_to_show = my_fruit_list.loc[fruits_selected]

# show df
st.dataframe(fruits_to_show)
