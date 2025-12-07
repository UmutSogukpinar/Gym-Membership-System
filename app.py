import streamlit as st
import sqlite3
import pandas as pd
from database import DATABASE_NAME, create_tables
from insert_data import insert_sample_data 
from queries import get_custom_query
from insertion import render_insert_page
from update import render_update_page
from delete import render_delete_page

conn = sqlite3.connect(DATABASE_NAME)
cur = conn.cursor()

# Create a flag table to track initialization status
cur.execute('''CREATE TABLE IF NOT EXISTS Init_Flags (
    key TEXT PRIMARY KEY,
    value TEXT
)''')

# Check if sample data has already been inserted
cur.execute("SELECT value FROM Init_Flags WHERE key = 'sample_data'")
result = cur.fetchone()

# If no sample data exists, create tables and insert sample data
if result is None:
    from database import create_tables
    from insert_data import insert_sample_data

    create_tables()
    insert_sample_data()
    # Mark that sample data has been inserted
    cur.execute("INSERT INTO Init_Flags (key, value) VALUES (?, ?)", ('sample_data', 'true'))
    conn.commit()

conn.close()

# ============================================
# Streamlit UI Configuration
# ============================================

PAGE_CONFIG_HEADER : str = "Gym Management"
PAGE_CONFIG_LAYOUT : str = "wide"
MAIN_PAGE_TITLE : str = "🏋️ Gym Management Panel"
SIDEBAR_HEADER : str = "Navigation"

st.set_page_config(page_title=PAGE_CONFIG_HEADER, layout=PAGE_CONFIG_LAYOUT)
st.title(MAIN_PAGE_TITLE)

# Create sidebar navigation
st.sidebar.header(SIDEBAR_HEADER)
menu : str = st.sidebar.radio(
    "Select Action",
    ["Home", "View Tables", "Insertion", "Update", "Delete"]
)

# ============================================
# Display selected page
# ============================================

if menu == "Home":
    st.markdown("""
    ### Welcome!
    Use the sidebar to manage the gym database.
    You can add, update, delete or explore membership data.
    """)

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
        query = get_custom_query(selected_table)
        df = pd.read_sql_query(query, conn)

        st.markdown(f"### Data for: **{selected_table}**")
        st.dataframe(df, use_container_width=True)

    except Exception as e:
        st.error(f"Error reading from table {selected_table}: {e}")
    finally:
        conn.close()

elif menu == "Insertion":
    render_insert_page()

elif menu == "Update":
    render_update_page()

elif menu == "Delete":
    render_delete_page()