import streamlit as st
import sqlite3
from database import DATABASE_NAME

def get_options(query):
    """
    Helper function to fetch dropdown options.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    cur.execute(query)
    data = cur.fetchall()
    conn.close()
    return {row[0]: row[1] for row in data} if data else {}

def render_delete_page():
    """
    Page for deleting records.
    Implements 'Cascade Deletion' logic: it automatically removes related
    dependencies (child records) before deleting the main record to prevent errors.
    """
    st.header("Delete Records (Force Delete)")
    st.warning("WARNING: These actions will permanently remove the record AND all its related history (Payments, Attendance, etc.). This cannot be undone.")

    menu_options = [
        "Delete Member",
        "Delete Trainer",
        "Cancel Class Session",
        "Remove Membership Package"
    ]

    choice = st.selectbox("Select Deletion Type", menu_options)

    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    
    # ==========================================
    # DELETE MEMBER
    # ==========================================
    if choice == "Delete Member":
        st.subheader("Delete Member & All History")

        member_map = get_options("""
            SELECT p.first_name || ' ' || p.last_name || ' (ID: ' || m.member_id || ')', m.member_id
            FROM Member m JOIN Person p ON m.person_id = p.id
        """)

        if not member_map:
            st.info("No members found.")
        else:
            selected_member = st.selectbox("Select Member", list(member_map.keys()))
            member_id = member_map[selected_member]

            st.error(f"Deleting **{selected_member}** will also delete their Payments, Check-ins, and Memberships.")

            if st.button("Confirm Force Delete"):
                try:
                    # Delete Dependencies (Children)
                    cur.execute("DELETE FROM Check_in WHERE member_id = ?", (member_id,))
                    cur.execute("DELETE FROM Attends WHERE member_id = ?", (member_id,))
                    cur.execute("DELETE FROM Payment WHERE member_id = ?", (member_id,))
                    cur.execute("DELETE FROM Membership WHERE member_id = ?", (member_id,))
                    
                    # Delete Member (Parent)
                    cur.execute("DELETE FROM Member WHERE member_id = ?", (member_id,))
                    

                    conn.commit()
                    st.success(f"Member and all related data deleted successfully!")
                    st.rerun()
                except Exception as e:
                    conn.rollback()
                    st.error(f"Error during deletion: {e}")

    # ==========================================
    # DELETE TRAINER
    # ==========================================
    elif choice == "Delete Trainer":
        st.subheader("Delete Trainer")

        trainer_map = get_options("""
            SELECT p.first_name || ' ' || p.last_name, t.trainer_id
            FROM Trainer t JOIN Person p ON t.person_id = p.id
        """)

        if not trainer_map:
            st.info("No trainers found.")
        else:
            selected_trainer = st.selectbox("Select Trainer", list(trainer_map.keys()))
            trainer_id = trainer_map[selected_trainer]

            st.error(f"Deleting **{selected_trainer}** will unassign them from all classes.")

            if st.button("Confirm Force Delete"):
                try:
                    # Delete Dependencies
                    cur.execute("DELETE FROM Teaches WHERE trainer_id = ?", (trainer_id,))
                    cur.execute("DELETE FROM Trainer_Specialization WHERE trainer_id = ?", (trainer_id,))
                    
                    # Delete Trainer
                    cur.execute("DELETE FROM Trainer WHERE trainer_id = ?", (trainer_id,))
                    
                    conn.commit()
                    st.success("Trainer deleted successfully!")
                    st.rerun()
                except Exception as e:
                    conn.rollback()
                    st.error(f"Error: {e}")

    # ==========================================
    # CANCEL CLASS SESSION
    # ==========================================
    elif choice == "Cancel Class Session":
        st.subheader("Cancel Session")

        session_map = get_options("""
            SELECT c.class_name || ' (' || cs.start_time || ')', cs.class_session_id
            FROM Class_Session cs
            JOIN Class c ON cs.class_id = c.class_id
            ORDER BY cs.start_time DESC
        """)

        if not session_map:
            st.info("No sessions found.")
        else:
            selected_session = st.selectbox("Select Session", list(session_map.keys()))
            session_id = session_map[selected_session]

            st.error(f"This will cancel the session **{selected_session}** and remove all attendance records.")

            if st.button("Confirm Cancel"):
                try:
                    # Delete Dependencies
                    cur.execute("DELETE FROM Check_in WHERE class_session_id = ?", (session_id,))
                    cur.execute("DELETE FROM Attends WHERE class_session_id = ?", (session_id,))
                    cur.execute("DELETE FROM Teaches WHERE class_session_id = ?", (session_id,))
                    
                    # Delete Session
                    cur.execute("DELETE FROM Class_Session WHERE class_session_id = ?", (session_id,))
                    
                    conn.commit()
                    st.success("Session cancelled and removed from calendar.")
                    st.rerun()
                except Exception as e:
                    conn.rollback()
                    st.error(f"Error: {e}")

    # ==========================================
    # REMOVE MEMBERSHIP
    # ==========================================
    elif choice == "Remove Membership Package":
        st.subheader("Delete Membership Record")

        mship_map = get_options("""
            SELECT (p.first_name || ' ' || p.last_name || ' - ' || mt.name || 
                    ' (End: ' || ms.end_date || ')'), ms.membership_id
            FROM Membership ms
            JOIN Member m ON ms.member_id = m.member_id
            JOIN Person p ON m.person_id = p.id
            JOIN Membership_Type mt ON ms.membership_type_id = mt.membership_type_id
        """)

        if not mship_map:
            st.info("No memberships found.")
        else:
            sel_mship = st.selectbox("Select Membership", list(mship_map.keys()))
            ms_id = mship_map[sel_mship]

            if st.button("Delete"):
                try:
                    cur.execute("DELETE FROM Membership WHERE membership_id = ?", (ms_id,))
                    conn.commit()
                    st.success("Membership record deleted.")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    conn.close()