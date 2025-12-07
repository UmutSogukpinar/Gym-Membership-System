import streamlit as st
import sqlite3
from datetime import datetime, timedelta
from database import DATABASE_NAME
from insertion import get_options

def render_update_page():
    """
    Page for updating existing records in the gym management system.
    Allows modifications to member details, trainer info, class schedules, and membership validity.
    """
    st.header("🔄 Update Records")

    # Menu options for different update operations
    menu_options = [
        "Update Member Profile",
        "Update Trainer Profile",
        "Reschedule Class Session",
        "Update Membership Validity"
    ]
    
    choice = st.selectbox("Select Update Type", menu_options)

    # Database connection for all update operations
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    cur.execute("PRAGMA foreign_keys = ON;")

    # ==========================================
    # UPDATE MEMBER PROFILE
    # ==========================================
    # Allow modification of member contact information and status
    if choice == "Update Member Profile":
        st.subheader("✏️ Edit Member Details")

        # Fetch list of members for selection
        member_map = get_options("""
            SELECT p.first_name || ' ' || p.last_name || ' (ID: ' || m.member_id || ')', m.member_id
            FROM Member m JOIN Person p ON m.person_id = p.id
        """)

        if not member_map:
            st.warning("No members found to update.")
        else:
            selected_member_name = st.selectbox("Select Member to Edit", list(member_map.keys()))
            member_id = member_map[selected_member_name]

            # Fetch current member information
            cur.execute("""
                SELECT p.email, p.city, p.street, p.zip, m.member_status, p.id
                FROM Member m 
                JOIN Person p ON m.person_id = p.id 
                WHERE m.member_id = ?
            """, (member_id,))
            
            data = cur.fetchone()
            
            if data:
                curr_email, curr_city, curr_street, curr_zip, curr_status, person_id = data

                with st.form("update_member_form"):
                    st.info(f"Editing: {selected_member_name}")
                    
                    col1, col2 = st.columns(2)
                    new_email = col1.text_input("Email", value=curr_email)
                    new_city = col2.text_input("City", value=curr_city)
                    
                    col3, col4 = st.columns(2)
                    new_street = col3.text_input("Street", value=curr_street)
                    new_zip = col4.text_input("Zip Code", value=curr_zip)
                    
                    status_opts = ["active", "inactive", "banned", "pending"]
                    curr_idx = status_opts.index(curr_status) if curr_status in status_opts else 0
                    new_status = st.selectbox("Member Status", status_opts, index=curr_idx)

                    submitted = st.form_submit_button("Update Member Info")

                    if submitted:
                        # Validate that required fields are not empty
                        # .strip() also prevents whitespace-only input
                        if not (new_email.strip() and new_city.strip() and new_street.strip() and new_zip.strip()):
                            st.error("Error: Fields (Email, City, Street, Zip) cannot be empty!")
                        else:
                            try:
                                cur.execute("""
                                    UPDATE Person 
                                    SET email=?, city=?, street=?, zip=? 
                                    WHERE id=?
                                """, (new_email.strip(), new_city.strip(), new_street.strip(), new_zip.strip(), person_id))

                                cur.execute("""
                                    UPDATE Member 
                                    SET member_status=? 
                                    WHERE member_id=?
                                """, (new_status, member_id))

                                conn.commit()
                                st.success("Member profile updated successfully!")
                            except Exception as e:
                                st.error(f"Update Error: {e}")

    # ==========================================
    # UPDATE TRAINER PROFILE
    # ==========================================
    # Allow modification of trainer specialization, email, and employment status
    elif choice == "Update Trainer Profile":
        st.subheader("💪 Edit Trainer Details")

        # Fetch list of trainers for selection
        trainer_map = get_options("""
            SELECT p.first_name || ' ' || p.last_name, t.trainer_id
            FROM Trainer t JOIN Person p ON t.person_id = p.id
        """)

        if trainer_map:
            selected_trainer = st.selectbox("Select Trainer", list(trainer_map.keys()))
            trainer_id = trainer_map[selected_trainer]

            cur.execute("""
                SELECT t.specialization, t.trainer_status, p.email
                FROM Trainer t JOIN Person p ON t.person_id = p.id
                WHERE t.trainer_id = ?
            """, (trainer_id,))
            
            row = cur.fetchone()
            if row:
                curr_spec, curr_status, curr_email = row

                # Handle NULL values from database
                # Convert None values to empty strings to prevent form errors
                val_spec = curr_spec if curr_spec is not None else ""
                val_email = curr_email if curr_email is not None else ""

                with st.form("update_trainer_form"):
                    # Use safe variables for form inputs
                    new_spec = st.text_input("Specialization", value=val_spec)
                    new_email = st.text_input("Email", value=val_email)
                    
                    status_opts = ["active", "on_leave", "terminated"]
                    curr_idx = status_opts.index(curr_status) if curr_status in status_opts else 0
                    new_status = st.selectbox("Employment Status", status_opts, index=curr_idx)

                    submitted = st.form_submit_button("Update Trainer")

                    if submitted:
                        if not (new_spec.strip() and new_email.strip()):
                            st.error("⚠️ Specialization and Email cannot be empty!")
                        else:
                            try:
                                cur.execute("UPDATE Trainer SET specialization=?, trainer_status=? WHERE trainer_id=?", 
                                            (new_spec.strip(), new_status, trainer_id))
                                
                                conn.commit()
                                st.success("Trainer info updated!")
                            except Exception as e:
                                st.error(f"Error: {e}")

    # ==========================================
    # RESCHEDULE CLASS SESSION
    # ==========================================
    # Allow modification of class session schedule, time, and capacity
    elif choice == "Reschedule Class Session":
        st.subheader("📅 Reschedule / Edit Session")

        # Fetch list of class sessions for selection
        session_map = get_options("""
            SELECT c.class_name || ' (' || cs.start_time || ')', cs.class_session_id
            FROM Class_Session cs 
            JOIN Class c ON cs.class_id = c.class_id
            ORDER BY cs.start_time DESC
        """)

        if not session_map:
            st.warning("No class sessions found.")
        else:
            selected_session = st.selectbox("Select Session to Edit", list(session_map.keys()))
            session_id = session_map[selected_session]

            cur.execute("SELECT start_time, end_time, capacity FROM Class_Session WHERE class_session_id=?", (session_id,))
            row = cur.fetchone()
            
            if row:
                try:
                    curr_start_dt = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                    curr_end_dt = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
                except:
                    curr_start_dt = datetime.now()
                    curr_end_dt = datetime.now()

                with st.form("update_session_form"):
                    col1, col2 = st.columns(2)
                    new_date = col1.date_input("Date", value=curr_start_dt.date())
                    
                    # Create base time options in 15-minute intervals
                    # Generate times from 00:00 to 23:45
                    base_time_options = []
                    base_day = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
                    for i in range(0, 24*60, 15): 
                        base_time_options.append((base_day + timedelta(minutes=i)).time())
                    
                    # Start time selection
                    # Copy list to avoid reference issues
                    start_opts = base_time_options.copy()
                    
                    # Add database time if not in standard options (e.g., 14:41)
                    if curr_start_dt.time() not in start_opts:
                        start_opts.append(curr_start_dt.time())
                        start_opts.sort()
                    
                    try:
                        st_idx = start_opts.index(curr_start_dt.time())
                    except ValueError:
                        st_idx = 0

                    new_start_time = col2.selectbox(
                        "Start Time", 
                        start_opts, 
                        index=st_idx,
                        format_func=lambda t: t.strftime("%H:%M")
                    )

                    col3, col4 = st.columns(2)

                    # End time selection (similar to start time)
                    end_opts = base_time_options.copy()
                    
                    # Add database end time if not in standard options
                    if curr_end_dt.time() not in end_opts:
                        end_opts.append(curr_end_dt.time())
                        end_opts.sort()

                    try:
                        et_idx = end_opts.index(curr_end_dt.time())
                    except ValueError:
                        et_idx = 0

                    new_end_time = col3.selectbox(
                        "End Time", 
                        end_opts, 
                        index=et_idx,
                        format_func=lambda t: t.strftime("%H:%M")
                    )
                    
                    new_capacity = col4.number_input("Capacity", value=row[2], min_value=1)

                    if st.form_submit_button("Update Session"):
                        # Validate time logic
                        # Ensure end time is after start time
                        if new_end_time <= new_start_time:
                            st.error("⚠️ Error: End time must be later than start time!")
                        else:
                            new_start_str = f"{new_date} {new_start_time}"
                            new_end_str = f"{new_date} {new_end_time}"
                            
                            dt_start = datetime.combine(new_date, new_start_time)
                            dt_end = datetime.combine(new_date, new_end_time)
                            new_duration = (dt_end - dt_start).seconds // 60

                            try:
                                cur.execute("""
                                    UPDATE Class_Session 
                                    SET start_time=?, end_time=?, capacity=?, duration=?
                                    WHERE class_session_id=?
                                """, (new_start_str, new_end_str, new_capacity, new_duration, session_id))
                                conn.commit()
                                st.success(f"Session updated! ({new_start_time} - {new_end_time})")
                            except Exception as e:
                                st.error(f"Error: {e}")

    # ==========================================
    # UPDATE MEMBERSHIP VALIDITY
    # ==========================================
    # Allow extension or modification of membership validity dates and status
    elif choice == "Update Membership Validity":
        st.subheader("💳 Extend or Update Membership")

        # Fetch list of active memberships with member and type information
        mship_map = get_options("""
            SELECT p.first_name || ' ' || p.last_name || ' - ' || mt.name || ' (End: ' || ms.end_date || ')', ms.membership_id
            FROM Membership ms
            JOIN Member m ON ms.member_id = m.member_id
            JOIN Person p ON m.person_id = p.id
            JOIN Membership_Type mt ON ms.membership_type_id = mt.membership_type_id
        """)

        if mship_map:
            sel_mship = st.selectbox("Select Membership", list(mship_map.keys()))
            ms_id = mship_map[sel_mship]

            cur.execute("SELECT start_date, end_date, is_active FROM Membership WHERE membership_id=?", (ms_id,))
            ms_row = cur.fetchone()

            if ms_row:
                try:
                    s_date_obj = datetime.strptime(ms_row[0], '%Y-%m-%d').date()
                    e_date_obj = datetime.strptime(ms_row[1], '%Y-%m-%d').date()
                except:
                    s_date_obj = datetime.today()
                    e_date_obj = datetime.today()

                with st.form("update_mship"):
                    st.write(f"Start Date: {s_date_obj}")
                    new_end_date = st.date_input("New End Date", value=e_date_obj)
                    new_active = st.checkbox("Is Active?", value=bool(ms_row[2]))

                    if st.form_submit_button("Update Membership"):
                        # Validate date logic
                        if new_end_date < s_date_obj:
                             st.error("Error: End date cannot be before start date!")
                        else:
                            try:
                                cur.execute("""
                                    UPDATE Membership 
                                    SET end_date=?, is_active=?
                                    WHERE membership_id=?
                                """, (str(new_end_date), 1 if new_active else 0, ms_id))
                                conn.commit()
                                st.success("Membership updated!")
                            except Exception as e:
                                st.error(f"Error: {e}")

    conn.close()