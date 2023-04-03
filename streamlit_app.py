
import streamlit
import pandas
import requests
import snowflake.connector

streamlit.set_page_config(layout="wide")
streamlit.title('My Parents New Healthy Diner');
streamlit.header("Breakfast Menu");
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal");
streamlit.text(" 🥗 Kale, Spinach & Rocket Smoothie");
streamlit.text(" 🐔Hard-Boiled Free-Range Egg");
streamlit.text("🥑🍞 Avacado Toast");
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list=pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list=my_fruit_list.set_index('Fruit')
#Let's put a picklist here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:",list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
#display the table on the page
streamlit.dataframe(fruits_to_show)


#New section to display fruityvice api response
streamlit.header('Fruityvice Fruit advice')
fruit_choice=streamlit.text_input('What fruit would you like information about?','kiwi')
streamlit.write('The user entered',fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
#streamlit.text(fruityvice_response)
#streamlit.text(fruityvice_response.json())

#take the json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#display the normalized data in screen
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur=my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
#my_data_row=my_cur.fetchone()
my_data_row=my_cur.fetchall()
streamlit.text("The fruit load list contains")
#streamlit.text(my_data_row)
streamlit.dataframe(my_data_row)

fruit_choice2=streamlit.text_input('What fruit would you like to add?','apple')
streamlit.write('Thanks for adding '+fruit_choice2)

my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('from streamlit')")