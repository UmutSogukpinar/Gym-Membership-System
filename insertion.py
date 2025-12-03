import streamlit as st
import sqlite3
from database import DATABASE_NAME

def render_insert_page():

    st.header("New Record Registration")
    
    # Selection Menu
    choice = st.selectbox(
        "Select Registration Type",
        ["New Member Registration", "New Trainer Registration", "Create New Class"]
    )

    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()

    # ==========================================
    # NEW MEMBER REGISTRATION
    # ==========================================
    if choice == "New Member Registration":
        st.subheader("Member Details")
        
        with st.form("add_member_full"):
            # --- Personal Info ---
            st.markdown("##### Personal Information")
            col1, col2 = st.columns(2)
            f_name = col1.text_input("First Name *")
            l_name = col2.text_input("Last Name *")
            email = st.text_input("Email *")
            birth_date = st.date_input("Birth Date")
            
            # --- Address & Phone ---
            st.markdown("##### Address & Contact")
            col3, col4 = st.columns(2)
            phone = col3.text_input("Personal Phone Number *")
            city = col4.text_input("City *")
            street = st.text_input("Street Address *")
            zip_code = st.text_input("Zip Code *")

            # --- Membership Info ---
            st.markdown("##### Membership Details")
            status = st.selectbox("Member Status", ["active", "inactive", "pending", "banned"])

            # --- Emergency Contact ---
            st.markdown("---")
            st.markdown("##### Emergency Contact")
            st.info("Required for safety regulations.")
            
            ec_col1, ec_col2 = st.columns(2)
            contact_name = ec_col1.text_input("Contact Name (Relative) *")
            relationship = ec_col2.text_input("Relationship *")
            contact_phone = st.text_input("Emergency Contact Phone *")

            submitted = st.form_submit_button("Register Member")

            if submitted:
                if (f_name and l_name and email and phone and city and street and zip_code 
                    and contact_name and relationship and contact_phone):
                    
                    try:
                        # Insert into PERSON
                        cur.execute('''
                            INSERT INTO Person (first_name, last_name, birth_date, email, city, street, zip)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (f_name, l_name, str(birth_date), email, city, street, zip_code))
                        
                        new_person_id = cur.lastrowid
                        
                        # Insert Person's PHONE
                        cur.execute('''
                            INSERT INTO Phone (owner_type, owner_id, phone_number, type)
                            VALUES (?, ?, ?, ?)
                        ''', ('person', new_person_id, phone, 'mobile'))

                        # Insert into MEMBER
                        cur.execute('''
                            INSERT INTO Member (person_id, member_status)
                            VALUES (?, ?)
                        ''', (new_person_id, status))

                        # Insert into CONTACT
                        cur.execute('''
                            INSERT INTO Contact (person_id, contact_name, relationship)
                            VALUES (?, ?, ?)
                        ''', (new_person_id, contact_name, relationship))
                        
                        new_contact_id = cur.lastrowid

                        # Insert Contact's PHONE
                        cur.execute('''
                            INSERT INTO Phone (owner_type, owner_id, phone_number, type)
                            VALUES (?, ?, ?, ?)
                        ''', ('contact', new_contact_id, contact_phone, 'mobile'))

                        conn.commit()
                        st.success(f"Member {f_name} {l_name} successfully registered!")
                        
                    except Exception as e:
                        st.error(f"Database Error: {e}")
                else:
                    st.error("All fields are required! Please fill in every input box.")

    # ==========================================
    # NEW TRAINER REGISTRATION
    # ==========================================
    elif choice == "New Trainer Registration":
        st.subheader("💪 Trainer Details")
        
        with st.form("add_trainer_full"):
            # --- Personal Info ---
            st.markdown("##### Personal Information")
            col1, col2 = st.columns(2)
            f_name = col1.text_input("First Name *")
            l_name = col2.text_input("Last Name *")
            email = st.text_input("Email *")
            birth_date = st.date_input("Birth Date")
            
            # --- Address & Phone ---
            st.markdown("##### Address & Contact")
            col3, col4 = st.columns(2)
            phone = col3.text_input("Personal Phone Number *")
            city = col4.text_input("City *")
            street = st.text_input("Street Address *")
            zip_code = st.text_input("Zip Code *")

            # --- Trainer Info ---
            st.markdown("##### Professional Details")
            t_col1, t_col2 = st.columns(2)
            specialization = t_col1.text_input("Specialization *")
            hire_date = t_col2.date_input("Hire Date")
            t_status = st.selectbox("Employment Status", ["active", "on_leave", "terminated"])

            # --- Emergency Contact ---
            st.markdown("---")
            st.markdown("##### Emergency Contact")
            
            ec_col1, ec_col2 = st.columns(2)
            contact_name = ec_col1.text_input("Contact Name *")
            relationship = ec_col2.text_input("Relationship *")
            contact_phone = st.text_input("Contact Phone Number *")

            submitted = st.form_submit_button("Register Trainer")

            if submitted:
                if (f_name and l_name and email and phone and city and street and zip_code 
                    and specialization and contact_name and relationship and contact_phone):
                    
                    try:
                        # Insert into PERSON
                        cur.execute('''
                            INSERT INTO Person (first_name, last_name, birth_date, email, city, street, zip)
                            VALUES (?, ?, ?, ?, ?, ?, ?)
                        ''', (f_name, l_name, str(birth_date), email, city, street, zip_code))
                        
                        new_person_id = cur.lastrowid
                        
                        # Insert Person's PHONE
                        cur.execute('''
                            INSERT INTO Phone (owner_type, owner_id, phone_number, type)
                            VALUES (?, ?, ?, ?)
                        ''', ('person', new_person_id, phone, 'mobile'))

                        # Insert into TRAINER
                        cur.execute('''
                            INSERT INTO Trainer (person_id, specialization, hire_date, trainer_status)
                            VALUES (?, ?, ?, ?)
                        ''', (new_person_id, specialization, str(hire_date), t_status))

                        # Insert into CONTACT
                        cur.execute('''
                            INSERT INTO Contact (person_id, contact_name, relationship)
                            VALUES (?, ?, ?)
                        ''', (new_person_id, contact_name, relationship))
                        
                        new_contact_id = cur.lastrowid

                        # Insert Contact's PHONE
                        cur.execute('''
                            INSERT INTO Phone (owner_type, owner_id, phone_number, type)
                            VALUES (?, ?, ?, ?)
                        ''', ('contact', new_contact_id, contact_phone, 'mobile'))

                        conn.commit()
                        st.success(f"Trainer {f_name} {l_name} successfully registered!")

                    except Exception as e:
                        st.error(f"Database Error: {e}")
                else:
                    st.error("All fields are required! Please fill in every input box.")

    # ==========================================
    # CREATE NEW CLASS
    # ==========================================
    elif choice == "Create New Class":
        st.subheader("Define a New Class Type")
        
        with st.form("add_class_simple"):
            c_name = st.text_input("Class Name (e.g. Morning Pilates) *")
            desc = st.text_area("Description *")
            
            submitted = st.form_submit_button("Create Class")

            if submitted:
                if c_name and desc:
                    try:
                        cur.execute('''
                            INSERT INTO Class (class_name, description)
                            VALUES (?, ?)
                        ''', (c_name, desc))
                        conn.commit()
                        st.success(f"Class '{c_name}' created successfully!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("Both Class Name and Description are required.")

    conn.close()