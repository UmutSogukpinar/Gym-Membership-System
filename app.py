import streamlit as st
import sqlite3
import pandas as pd
from database import DATABASE_NAME, create_tables
from insert_data import insert_sample_data 
from queries import get_custom_query

# Create tables if not exists
create_tables()

# Constant names
PAGE_CONFIG_HEADER : str = "Gym Management"
PAGE_CONFIG_LAYOUT : str = "wide"
MAIN_PAGE_TITLE : str = "🏋️ Gym Management Panel"
SIDEBAR_HEADER : str = "Navigation"

st.set_page_config(page_title=PAGE_CONFIG_HEADER, layout=PAGE_CONFIG_LAYOUT)
st.title(MAIN_PAGE_TITLE)

st.sidebar.header(SIDEBAR_HEADER)
menu : str = st.sidebar.radio(
    "Select Action",
    ["Home", "View Tables", "Add New Person (INSERT)", "Update", "Delete", "Membership & Classes (JOIN)"]
)

if menu == "Home":
    st.markdown("""
    ### Welcome!
    Use the sidebar to manage the gym database
    You can add, update, delete or explore membership data.
    """)

    if st.button("Insert Sample Data"):
        insert_sample_data()
        st.success("Sample data inserted into the database successfully!")

elif menu == "View Tables":
    st.subheader("📋 View All Tables")
    
    table_names = [
        "Person", "Member", "Trainer", "Specialization", "Trainer_Specialization",
        "Contact", "Class", "Class_Session", "Membership_Type", "Membership",
        "Payment", "Check_in", "Attends", "Teaches"
    ]

    selected_table : str = st.sidebar.selectbox("Choose table:", table_names)

    conn : sqlite3.Connection = sqlite3.connect(DATABASE_NAME)
    
    try:
        # Get query
        query = get_custom_query(selected_table)
        
        # Get data
        df = pd.read_sql_query(query, conn)
        
        # Info
        st.markdown(f"### Data for: **{selected_table}**")
                
        # Show table
        st.dataframe(df, use_container_width=True)
        
    except Exception as e:
        st.error(f"Error reading from table {selected_table}: {e}")
    finally:
        conn.close()

elif menu == "Add New Person (INSERT)":
    st.info("To be continued..")

elif menu == "Membership & Classes (JOIN)":
    st.info("To be continued..")
