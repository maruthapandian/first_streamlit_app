
import streamlit
import pandas

streamlit.title('My Parents New Healthy Diner');
streamlit.header("Breakfast Menu");
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal");
streamlit.text(" 🥗 Kale, Spinach & Rocket Smoothie");
streamlit.text(" 🐔Hard-Boiled Free-Range Egg");
streamlit.text("🥑🍞 Avacado Toast");
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruits_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
#Let's put a picklist here so they can pick the fruit they want to include
streamlit.multiselect("Pick some fruits:",list(my_fruits_list.index))
streamlit.dataframe(my_fruits_list)