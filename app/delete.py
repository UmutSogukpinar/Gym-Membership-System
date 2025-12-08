import streamlit as st
import sqlite3
from database import DATABASE_NAME
from insertion import get_options

def render_delete_page():
    """
    Page for deleting records from the gym management system.
    Provides options to remove members, trainers, sessions, and membership records.
    All deletions are permanent and require confirmation.
    """
    st.header("Delete Records")
    st.warning("Warning: These actions are permanent and cannot be undone!")

    # Menu options for different deletion operations
    menu_options = [
        "Delete Member",
        "Delete Trainer",
        "Cancel Class Session",
        "Remove Membership Package"
    ]
    
    choice = st.selectbox("Select Deletion Type", menu_options)

    # Database connection for deletion operations
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()
    
    # Enable foreign key constraints
    # This ensures the database prevents deletion if related records exist
    cur.execute("PRAGMA foreign_keys = ON;")

    # ==========================================
    # DELETE MEMBER
    # ==========================================
    # Allow removal of member records while preserving person data
    if choice == "Delete Member":
        st.subheader("Delete a Member")

        # Fetch list of members with their IDs for selection
        member_map = get_options("""
            SELECT p.first_name || ' ' || p.last_name || ' (ID: ' || m.member_id || ')', m.member_id
            FROM Member m JOIN Person p ON m.person_id = p.id
        """)

        if not member_map:
            st.info("No members found to delete.")
        else:
            selected_member = st.selectbox("Select Member to Delete", list(member_map.keys()))
            member_id = member_map[selected_member]

            st.error(f"You are about to delete: **{selected_member}**")
            
            with st.expander("ℹ️ Why can't I delete some members?"):
                st.write("""
                If a member has related records (Payments, Attendances, Memberships), 
                the database prevents deletion to keep data safe. 
                You must delete those related records first.
                """)

            if st.button("Confirm Delete Member"):
                try:
                    # Delete only the Member record
                    # Keep the Person record with address and phone information
                    cur.execute("DELETE FROM Member WHERE member_id = ?", (member_id,))
                    conn.commit()
                    st.success(f"Member record for {selected_member} deleted successfully!")
                    st.rerun()  # Refresh the page
                except sqlite3.IntegrityError:
                    st.error("⚠️ Cannot delete this member! They have linked data (Payments, Memberships, etc.).")
                except Exception as e:
                    st.error(f"Error: {e}")

    # ==========================================
    # DELETE TRAINER
    # ==========================================
    # Allow removal of trainer records with validation for related assignments
    elif choice == "Delete Trainer":
        st.subheader("Delete a Trainer")

        trainer_map = get_options("""
            SELECT p.first_name || ' ' || p.last_name, t.trainer_id
            FROM Trainer t JOIN Person p ON t.person_id = p.id
        """)

        if not trainer_map:
            st.info("No trainers found.")
        else:
            selected_trainer = st.selectbox("Select Trainer", list(trainer_map.keys()))
            trainer_id = trainer_map[selected_trainer]

            st.error(f"You are about to delete trainer: **{selected_trainer}**")

            if st.button("Confirm Delete Trainer"):
                try:
                    cur.execute("DELETE FROM Trainer WHERE trainer_id = ?", (trainer_id,))
                    conn.commit()
                    st.success("Trainer record deleted!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("⚠️ Cannot delete! This trainer is assigned to classes or has specializations.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # ==========================================
    # CANCEL CLASS SESSION
    # ==========================================
    # Allow cancellation of scheduled class sessions
    elif choice == "Cancel Class Session":
        st.subheader("Cancel a Scheduled Session")

        # Retrieve all class sessions (not just future ones)
        session_map = get_options("""
            SELECT c.class_name || ' (' || cs.start_time || ')', cs.class_session_id
            FROM Class_Session cs 
            JOIN Class c ON cs.class_id = c.class_id
            ORDER BY cs.start_time DESC
        """)

        if not session_map:
            st.info("No sessions found.")
        else:
            selected_session = st.selectbox("Select Session to Cancel", list(session_map.keys()))
            session_id = session_map[selected_session]

            st.error(f"Deleting session: **{selected_session}**")

            if st.button("Confirm Cancel Session"):
                try:
                    cur.execute("DELETE FROM Class_Session WHERE class_session_id = ?", (session_id,))
                    conn.commit()
                    st.success("Class session cancelled/deleted successfully!")
                    st.rerun()
                except sqlite3.IntegrityError:
                    st.error("⚠️ Cannot delete! There are members registered (Attends) or Checked-in to this session.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # ==========================================
    # REMOVE MEMBERSHIP PACKAGE
    # ==========================================
    # Allow removal of membership records from history
    elif choice == "Remove Membership Package":
        st.subheader("❌ Delete a Membership Record")

        mship_map = get_options("""
            SELECT p.first_name || ' ' || p.last_name || ' - ' || mt.name || ' (End: ' || ms.end_date || ')', ms.membership_id
            FROM Membership ms
            JOIN Member m ON ms.member_id = m.member_id
            JOIN Person p ON m.person_id = p.id
            JOIN Membership_Type mt ON ms.membership_type_id = mt.membership_type_id
        """)

        if not mship_map:
            st.info("No membership records found.")
        else:
            sel_mship = st.selectbox("Select Membership to Delete", list(mship_map.keys()))
            ms_id = mship_map[sel_mship]

            st.error("This will completely remove the membership record from history.")
            
            if st.button("Confirm Delete Membership"):
                try:
                    cur.execute("DELETE FROM Membership WHERE membership_id = ?", (ms_id,))
                    conn.commit()
                    st.success("Membership record deleted!")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

    conn.close()