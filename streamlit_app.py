# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
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

# Get active Snowflake session
session = get_active_session()

# Get fruit options
my_dataframe = session.table(
    "SMOOTHIES.PUBLIC.FRUIT_OPTIONS"
).select(
    col("FRUIT_NAME")
)

# Choose ingredients
ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe
)

if ingredients_list:

    st.write(ingredients_list)

    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + " "

    st.write(ingredients_string)

    # Insert order
    my_insert_stmt = """
        INSERT INTO SMOOTHIES.PUBLIC.ORDERS
        (INGREDIENTS, NAME_ON_ORDER)
        VALUES ('""" + ingredients_string + """','""" + name_on_order + """')
    """

    st.write(my_insert_stmt)

    # Submit button
    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()

        st.success(
            "Your Smoothie is ordered!",
            icon="✅"
        )
