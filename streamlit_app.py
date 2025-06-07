# Import python packages
import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie!")
st.write(
  """Choose the fruits you want customize your Smoothie!
  """
)



name_on_order = st.text_input("Name on Smoothie: ")
st.write("The name of your smoothie will be", name_on_order)


cnx=st.connection("snowflake")
session = cnx.session()
#session = get_active_session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()
#convert the  Snowpark Dataframe to a Pandas Dataframe so we can use the LOC function
pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop

ingredients_list=st.multiselect(
    'choose upto 5 ingredients', my_dataframe, max_selections=5)

if ingredients_list:
    ingredients_string= ''

    for fruit_choosen in ingredients_list:
        ingredients_string += fruit_choosen + ' '
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_choosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')
        
        st.subheader(fruit_choosen + ' Nutrition Information')
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_choosen)
        sf_df=st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
           #st.write(ingredients_string)

    my_insert_stmt = """INSERT INTO smoothies.public.orders(ingredients,name_on_order)
                VALUES ('""" + ingredients_string + """','""" + name_on_order + """')"""

    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert=st.button('Submit Order')
    
    if time_to_insert:
      session.sql(my_insert_stmt).collect()
    
      st.success('Your Smoothie is ordered!', icon="✅")



