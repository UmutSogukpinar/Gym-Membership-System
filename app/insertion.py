import streamlit as st
import sqlite3
from database import DATABASE_NAME
from datetime import datetime


def get_options(query):
    """
    Execute a query and return results as a dictionary mapping display names to IDs.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    conn.close()

    return {row[0]: row[1] for row in data} if data else {}


def render_insert_page():
    """
    Main page for inserting new records with STRICT INPUT VALIDATION.
    """
    st.header("Record Registration")

    menu_options = [
        "New Member Registration",
        "New Trainer Registration",
        "Create New Class",
        "Schedule Class Session",
        "Assign Membership",
        "Record Payment",
        "Assign Trainer Specialization"
    ]

    choice = st.selectbox("Select Registration Type", menu_options)

    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    # ==========================================
    # NEW MEMBER REGISTRATION
    # ==========================================
    if choice == "New Member Registration":
        st.subheader("Member Details")
        with st.form("add_member_full"):
            st.markdown("##### Personal Information")
            col1, col2 = st.columns(2)
            f_name = col1.text_input("First Name *")
            l_name = col2.text_input("Last Name *")
            email = st.text_input("Email *")
            birth_date = st.date_input("Birth Date")

            st.markdown("##### Address & Contact")
            col3, col4 = st.columns(2)
            phone = col3.text_input("Personal Phone Number *")
            city = col4.text_input("City *")
            street = st.text_input("Street Address *")
            zip_code = st.text_input("Zip Code *")

            st.markdown("##### Membership Status")
            status = st.selectbox("Member Status", ["active", "inactive", "pending"])

            st.markdown("##### Emergency Contact")
            ec_col1, ec_col2 = st.columns(2)
            contact_name = ec_col1.text_input("Contact Name (Relative) *")
            relationship = ec_col2.text_input("Relationship *")
            contact_phone = st.text_input("Emergency Contact Phone *")

            submitted = st.form_submit_button("Register Member")

            if submitted:
                # Validation List: All these must be True (not empty strings)
                required_fields = [
                    f_name,
                    l_name,
                    email,
                    phone,
                    city,
                    street,
                    zip_code,
                    contact_name,
                    relationship,
                    contact_phone]

                if all(required_fields):
                    try:
                        cur.execute('''INSERT INTO Person (first_name, last_name, birth_date, email, city, street, zip)
                                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                    (f_name, l_name, str(birth_date), email, city, street, zip_code))
                        new_person_id = cur.lastrowid

                        cur.execute('''INSERT INTO Phone (owner_type, owner_id, phone_number, type)
                                       VALUES (?, ?, ?, ?)''',
                                    ('person', new_person_id, phone, 'mobile'))

                        cur.execute('''INSERT INTO Member (person_id, member_status) VALUES (?, ?)''',
                                    (new_person_id, status))

                        cur.execute('''INSERT INTO Contact (person_id, contact_name, relationship)
                                       VALUES (?, ?, ?)''',
                                    (new_person_id, contact_name, relationship))
                        new_contact_id = cur.lastrowid

                        cur.execute('''INSERT INTO Phone (owner_type, owner_id, phone_number, type)
                                       VALUES (?, ?, ?, ?)''',
                                    ('contact', new_contact_id, contact_phone, 'mobile'))

                        conn.commit()
                        st.success(f"Member {f_name} {l_name} added successfully!")
                    except Exception as e:
                        st.error(f"Database Error: {e}")
                else:
                    st.error("Registration Failed: All fields marked with * are required.")

    # ==================================================
    # NEW TRAINER REGISTRATION
    # Enables registration of new fitness trainers with
    # personal details, contact information, and employment status
    # ==================================================
    elif choice == "New Trainer Registration":
        st.subheader("Trainer Details")
        with st.form("add_trainer_full"):
            st.markdown("##### Personal Information")
            col1, col2 = st.columns(2)
            f_name = col1.text_input("First Name *")
            l_name = col2.text_input("Last Name *")
            email = st.text_input("Email *")
            birth_date = st.date_input("Birth Date")

            st.markdown("##### Address & Contact")
            col3, col4 = st.columns(2)
            phone = col3.text_input("Personal Phone Number *")
            city = col4.text_input("City *")
            street = st.text_input("Street Address *")
            zip_code = st.text_input("Zip Code *")

            st.markdown("##### Professional Details")
            t_col1, t_col2 = st.columns(2)
            specialization = t_col1.text_input("Main Specialization (Text) *")
            hire_date = t_col2.date_input("Hire Date")
            t_status = st.selectbox("Employment Status", ["active", "on_leave", "terminated"])

            submitted = st.form_submit_button("Register Trainer")

            if submitted:
                # Validation
                required_fields = [f_name, l_name, email, phone, city, street, zip_code, specialization]

                if all(required_fields):
                    try:
                        cur.execute('''INSERT INTO Person (first_name, last_name, birth_date, email, city, street, zip)
                                       VALUES (?, ?, ?, ?, ?, ?, ?)''',
                                    (f_name, l_name, str(birth_date), email, city, street, zip_code))
                        new_person_id = cur.lastrowid

                        cur.execute('''INSERT INTO Phone (owner_type, owner_id, phone_number, type)
                                       VALUES (?, ?, ?, ?)''',
                                    ('person', new_person_id, phone, 'mobile'))

                        cur.execute('''INSERT INTO Trainer (person_id, specialization, hire_date, trainer_status)
                                       VALUES (?, ?, ?, ?)''',
                                    (new_person_id, specialization, str(hire_date), t_status))

                        conn.commit()
                        st.success(f"Trainer {f_name} {l_name} added successfully!")
                    except Exception as e:
                        st.error(f"Database Error: {e}")
                else:
                    st.error("Registration Failed: All fields marked with * are required.")

    # ==================================================
    # CREATE NEW CLASS
    # Allows creation of new class types with name and description.
    # These class types can later be scheduled for specific sessions
    # ==================================================
    elif choice == "Create New Class":
        st.subheader("Define a New Class Type")
        with st.form("add_class_simple"):
            c_name = st.text_input("Class Name (e.g. Morning Pilates) *")
            desc = st.text_area("Description *")
            submitted = st.form_submit_button("Create Class")

            if submitted:
                if c_name and desc:
                    try:
                        cur.execute("INSERT INTO Class (class_name, description) VALUES (?, ?)", (c_name, desc))
                        conn.commit()
                        st.success(f"Class '{c_name}' created!")
                    except Exception as e:
                        st.error(f"Error: {e}")
                else:
                    st.error("Both Class Name and Description are required.")

    # ==================================================
    # SCHEDULE CLASS SESSION
    # Assigns specific time slots and capacity limits to existing class types.
    # Each session represents a single class instance on a particular date and time
    # ==================================================
    elif choice == "Schedule Class Session":
        st.subheader("Schedule a Session")
        st.info("Assign a specific time and capacity to a Class Type.")

        class_map = get_options("SELECT class_name, class_id FROM Class")

        if not class_map:
            st.error("No classes defined yet! Please create a class first.")
        else:
            with st.form("schedule_session"):
                selected_class_name = st.selectbox("Select Class Type", list(class_map.keys()))

                col1, col2 = st.columns(2)
                date = col1.date_input("Date")
                time_start = col2.time_input("Start Time")

                col3, col4 = st.columns(2)
                duration = col3.number_input("Duration (minutes)", min_value=30, value=60)
                capacity = col4.number_input("Capacity", min_value=1, value=15)

                submitted = st.form_submit_button("Schedule Session")

                if submitted:
                    # Date/Time are usually returned as objects by Streamlit, so they are rarely empty,
                    # but we should ensure capacity and duration are logical.
                    if duration > 0 and capacity > 0:
                        start_datetime = f"{date} {time_start}"
                        class_id = class_map[selected_class_name]

                        try:
                            cur.execute('''
                                INSERT INTO Class_Session (class_id, start_time, end_time, capacity, duration)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (class_id, start_datetime, "Calculated based on duration", capacity, duration))
                            conn.commit()
                            st.success("Class Session Scheduled Successfully!")
                        except Exception as e:
                            st.error(f"Database Error: {e}")
                    else:
                        st.error("Invalid Capacity or Duration.")

    # ==================================================
    # ASSIGN MEMBERSHIP
    # Links membership packages to members with activation and expiration dates.
    # Members can have multiple active memberships simultaneously
    # ==================================================
    elif choice == "Assign Membership":
        st.subheader("Assign Membership Package")

        member_query = """
            SELECT p.first_name || ' ' || p.last_name || ' (ID: ' || m.member_id || ')', m.member_id
            FROM Member m JOIN Person p ON m.person_id = p.id
        """
        member_map = get_options(member_query)
        type_map = get_options("SELECT name || ' - ' || price || ' TL', membership_type_id FROM Membership_Type")

        if not member_map:
            st.error("No members found. Register a member first.")
        elif not type_map:
            st.error("No membership types found. Add them to DB first.")
        else:
            with st.form("assign_membership"):
                selected_member = st.selectbox("Select Member", list(member_map.keys()))
                selected_type = st.selectbox("Membership Type", list(type_map.keys()))

                col1, col2 = st.columns(2)
                start_d = col1.date_input("Start Date", value=datetime.today())
                end_d = col2.date_input("End Date", value=datetime.today())

                is_active = st.checkbox("Set as Active Immediately", value=True)

                submitted = st.form_submit_button("Assign Membership")

                if submitted:
                    if end_d < start_d:
                        st.error("Error: End date cannot be before start date!")
                    else:
                        m_id = member_map[selected_member]
                        mt_id = type_map[selected_type]

                        try:
                            cur.execute('''
                                INSERT INTO Membership (member_id, membership_type_id, is_active, start_date, end_date)
                                VALUES (?, ?, ?, ?, ?)
                            ''', (m_id, mt_id, 1 if is_active else 0, str(start_d), str(end_d)))
                            conn.commit()
                            st.success("Membership assigned successfully!")
                        except Exception as e:
                            st.error(f"Error: {e}")

    # ==================================================
    # RECORD PAYMENT
    # Processes and records financial transactions from members.
    # Supports multiple payment methods (Credit Card, Cash, Bank Transfer)
    # ==================================================
    elif choice == "Record Payment":
        st.subheader("Process Payment")

        member_query = """
            SELECT p.first_name || ' ' || p.last_name, m.member_id
            FROM Member m JOIN Person p ON m.person_id = p.id
        """
        member_map = get_options(member_query)

        if member_map:
            with st.form("pay_form"):
                selected_member = st.selectbox("Payer (Member)", list(member_map.keys()))
                amount = st.number_input("Amount (TL)", min_value=0.0, step=10.0)
                method = st.selectbox("Payment Method", ["Credit Card", "Cash", "Bank Transfer"])
                p_date = st.date_input("Payment Date")

                submitted = st.form_submit_button("Record Payment")

                if submitted:
                    # Enforce amount > 0
                    if amount > 0:
                        m_id = member_map[selected_member]
                        try:
                            cur.execute('''
                                INSERT INTO Payment (member_id, payment_date, method, amount)
                                VALUES (?, ?, ?, ?)
                            ''', (m_id, str(p_date), method, amount))
                            conn.commit()
                            st.success(f"Payment of {amount} TL recorded!")
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.error("Payment amount must be greater than 0.")
        else:
            st.warning("No members available to receive payment from.")

    # ==================================================
    # ASSIGN TRAINER SPECIALIZATION
    # Assigns specialized training areas to trainers.
    # A trainer can have multiple specializations (e.g., Yoga, Weightlifting, Cardio)
    # ==================================================
    elif choice == "Assign Trainer Specialization":
        st.subheader("Assign Specialization to Trainer")

        trainer_query = """
            SELECT p.first_name || ' ' || p.last_name, t.trainer_id
            FROM Trainer t JOIN Person p ON t.person_id = p.id
        """
        trainer_map = get_options(trainer_query)
        spec_map = get_options("SELECT name, specialization_id FROM Specialization")

        if not trainer_map:
            st.warning("No trainers found.")
        elif not spec_map:
            st.warning("No specializations defined in database.")
        else:
            with st.form("spec_form"):
                t_name = st.selectbox("Trainer", list(trainer_map.keys()))
                s_name = st.selectbox("Specialization Area", list(spec_map.keys()))

                submitted = st.form_submit_button("Assign")

                if submitted:
                    # Select boxes always return a value if the list is not empty,
                    # but handling the case just in case.
                    if t_name and s_name:
                        t_id = trainer_map[t_name]
                        s_id = spec_map[s_name]

                        try:
                            query = "INSERT INTO Trainer_Specialization (trainer_id, specialization_id) VALUES (?, ?)"
                            cur.execute(query, (t_id, s_id))
                            conn.commit()
                            st.success(f"Assigned {s_name} to {t_name}")
                        except sqlite3.IntegrityError:
                            st.error("This trainer already has this specialization.")
                        except Exception as e:
                            st.error(f"Error: {e}")
                    else:
                        st.error("Missing selections.")

    conn.close()
