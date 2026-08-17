# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write(
    """Choose the fruits you want in your custom Smoothie!"""
)

# Name on the smoothie
name_on_order = st.text_input("Name on Smoothie:")

st.write(
    "The name on your Smoothie will be:",
    name_on_order
)

# Connect to Snowflake
cnx = st.connection("snowflake")
session = cnx.session()

# Get fruit options
my_dataframe = session.table(
    "SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
).select(
    col("FRUIT_NAME")
).collect()

# Convert Snowflake rows into a list of fruit names
fruit_options = [row["FRUIT_NAME"] for row in my_dataframe]

# Choose ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_options,
    max_selections=5
)

if ingredients_list:

    st.write(ingredients_list)

    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

    st.write(ingredients_string)

    # Submit button
    time_to_insert = st.button("Submit Order")

    if time_to_insert:

        # Safely insert the order
        my_insert_stmt = """
            INSERT INTO SMOOTHIES.PUBLIC.ORDERS
            (INGREDIENTS, NAME_ON_ORDER)
            VALUES (?, ?)
        """

        session.sql(
            my_insert_stmt,
            params=[ingredients_string, name_on_order]
        ).collect()

        st.success(
            "Your Smoothie is ordered!",
            icon="✅"
        )
        
smoothiefroot_response = requests.get(
    "https://my.smoothiefroot.com/api/fruit/watermelon"
)

sf_df = pd.DataFrame(smoothiefroot_response.json())

st.dataframe(sf_df)
