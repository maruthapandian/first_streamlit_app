
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

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

#create the repeatable code block (called a function)
def get_fruityvice_data(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
        #streamlit.text(fruityvice_response)
        #streamlit.text(fruityvice_response.json())
        #take the json version of the response and normalize it
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized
        #display the normalized data in screen
        


#New section to display fruityvice api response
streamlit.header('Fruityvice Fruit advice')
try:
    fruit_choice=streamlit.text_input('What fruit would you like information about?')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        streamlit.write('The user entered',fruit_choice)
        back_from_function=get_fruityvice_data(fruit_choice)
        streamlit.dataframe(back_from_function)

except URLError as e:
    streamlit.error()

#dont run anything past here while we troubleshoot
#streamlit.stop()

streamlit.text("View Our Fruit List - Add Your Favorites!")
#snowfalke related functions
def get_fruit_load_list():
     with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()

#Add a button to load the fruit
if streamlit.button('Get Fruit List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows=get_fruit_load_list()
    my_cnx.close()
    streamlit.dataframe(my_data_rows)

#Allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values('"+new_fruit+"')")
        return 'Thanks for adding '+new_fruit
     
add_my_fruit=streamlit.text_input('What fruit would you like to add?')
if  streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function=insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    streamlit.text(back_from_function)

