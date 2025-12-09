def get_custom_query(table_name):
    """
    Return a formatted SQL query for displaying a specific table.
    Joins related tables to show comprehensive information for each entity.
    """
    
    # MEMBER Table - Display member information including Phone Number
    if table_name == "Member":
        return ("""
        SELECT 
            m.member_id, 
            p.first_name, 
            p.last_name, 
            p.email, 
            GROUP_CONCAT(ph.phone_number, ', ') as Phone_Number, -- Added Phone Column
            m.member_status 
        FROM Member m
        JOIN Person p ON m.person_id = p.id
        LEFT JOIN Phone ph ON p.id = ph.owner_id AND ph.owner_type = 'person'
        GROUP BY m.member_id
        """)

    # TRAINER Table - Display trainer details including Phone Number
    elif table_name == "Trainer":
        return ("""
        SELECT 
            t.trainer_id, 
            p.first_name || ' ' || p.last_name as Trainer_Name,
            GROUP_CONCAT(ph.phone_number, ', ') as Phone_Number, -- Added Phone Column
            t.specialization,
            t.hire_date, 
            t.trainer_status 
        FROM Trainer t
        JOIN Person p ON t.person_id = p.id
        LEFT JOIN Phone ph ON p.id = ph.owner_id AND ph.owner_type = 'person'
        GROUP BY t.trainer_id
        """)

    # MEMBERSHIP Table
    elif table_name == "Membership":
        return ("""
        SELECT 
            ms.membership_id,
            p.first_name || ' ' || p.last_name as Member_Name, 
            mt.name as Membership_Type, 
            mt.price,
            ms.is_active,
            ms.start_date,
            ms.end_date
        FROM Membership ms
        JOIN Member m ON ms.member_id = m.member_id
        JOIN Person p ON m.person_id = p.id
        JOIN Membership_Type mt ON ms.membership_type_id = mt.membership_type_id
        """)

    # CLASS_SESSION Table
    elif table_name == "Class_Session":
        return ("""
        SELECT 
            cs.class_session_id,
            c.class_name,
            c.description,
            cs.start_time,
            cs.end_time,
            cs.capacity
        FROM Class_Session cs
        JOIN Class c ON cs.class_id = c.class_id
        """)
        
    # PAYMENT Table
    elif table_name == "Payment":
        return ("""
        SELECT
            pay.payment_id,
            p.first_name || ' ' || p.last_name as Member_Name,
            pay.amount,
            pay.method,
            pay.payment_date
        FROM Payment pay
        JOIN Member m ON pay.member_id = m.member_id
        JOIN Person p ON m.person_id = p.id
        """)

    # PHONE Table
    elif table_name == "Phone":
        return ("""
        SELECT
            ph.phone_id,
            p.first_name || ' ' || p.last_name as Owner_Name,
            ph.phone_number,
            ph.type as Phone_Type
        FROM Phone ph
        LEFT JOIN Person p ON ph.owner_id = p.id
        WHERE ph.owner_type = 'person'
        """)

    # TRAINER_SPECIALIZATION Table
    elif table_name == "Trainer_Specialization":
        return ("""
        SELECT 
            p.first_name || ' ' || p.last_name as Trainer_Name, 
            s.name as Specialization_Area 
        FROM Trainer_Specialization ts
        JOIN Trainer t ON ts.trainer_id = t.trainer_id
        JOIN Person p ON t.person_id = p.id
        JOIN Specialization s ON ts.specialization_id = s.specialization_id
        """)

    # CONTACT Table
    elif table_name == "Contact":
        return ("""
        SELECT 
            c.contact_id,
            p.first_name || ' ' || p.last_name as Member_Name,
            c.contact_name as Emergency_Contact,
            c.relationship,
            GROUP_CONCAT(ph.phone_number, ', ') as Contact_Phones
        FROM Contact c
        JOIN Person p ON c.person_id = p.id
        LEFT JOIN Phone ph ON c.contact_id = ph.owner_id AND ph.owner_type = 'contact'
        GROUP BY c.contact_id
        """)

    elif table_name == "Attends":
        return ("""
        SELECT 
            p.first_name || ' ' || p.last_name as Member_Name,
            c.class_name as Class, 
            cs.start_time as Session_Time, 
            cs.duration || ' min' as Duration 
        FROM Attends a
        JOIN Member m ON a.member_id = m.member_id
        JOIN Person p ON m.person_id = p.id
        JOIN Class_Session cs ON a.class_session_id = cs.class_session_id
        JOIN Class c ON cs.class_id = c.class_id
        """)

    elif table_name == "Teaches":
        return ("""
        SELECT 
            p.first_name || ' ' || p.last_name as Trainer_Name, 
            c.class_name as Class, 
            cs.start_time as Session_Time, 
            cs.duration || ' min' as Duration 
        FROM Teaches t
        JOIN Trainer tr ON t.trainer_id = tr.trainer_id
        JOIN Person p ON tr.person_id = p.id
        JOIN Class_Session cs ON t.class_session_id = cs.class_session_id
        JOIN Class c ON cs.class_id = c.class_id
        """)
        
    elif table_name == "Check_in":
        return ("""
        SELECT
                ci.checkin_id,
                p.first_name || ' ' || p.last_name as Member_Name,
                c.class_name as Class,
                cs.start_time as Session_Scheduled,
                ci.checkin_time,
                ci.checkout_time
        FROM Check_in ci
        JOIN Member m ON ci.member_id = m.member_id
        JOIN Person p ON m.person_id = p.id
        JOIN Class_Session cs ON ci.class_session_id = cs.class_session_id
        JOIN Class c ON cs.class_id = c.class_id
        ORDER BY ci.checkin_time DESC
        """)

    else:
        return (f"SELECT * FROM {table_name}")