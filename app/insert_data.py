import sqlite3
from database import DATABASE_NAME


def insert_sample_data():
    """
    Populate the database with sample data for testing and demonstration.
    Creates sample persons, members, trainers, classes, and related records.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()

    # Enable foreign key constraints to maintain data integrity
    cur.execute("PRAGMA foreign_keys = ON;")

    # Insert person records - Base data for all individuals (members, trainers, etc.)
    people = [
        ("Ali", "Yıldız", "1990-01-01", "ali@gmail.com", "Istanbul", "Mecidiyeköy", "34387"),
        ("Zeynep", "Arslan", "1988-02-14", "zeynep@gmail.com", "Ankara", "Kızılay", "06000"),
        ("Kemal", "Demir", "1995-03-30", "kemal@gmail.com", "Izmir", "Alsancak", "35000"),
        ("Emir", "Salaman", "1992-06-11", "emri@gmail.com", "Bursa", "Nilüfer", "16000"),
        ("Ece", "Aksoy", "1987-09-19", "ece@gmail.com", "Adana", "Çukurova", "01000")
    ]

    # Insert each person with their contact information
    for i, person in enumerate(people, start=1):
        cur.execute('''
            INSERT OR IGNORE INTO Person (first_name, last_name, birth_date, email, city, street, zip)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', person)

        cur.execute('''
            INSERT OR IGNORE INTO Phone (owner_type, owner_id, phone_number, type)
            VALUES (?, ?, ?, ?)
        ''', ('person', i, f'+90555{i:07d}', 'mobile'))

        # Create emergency contact for each person
        contact_name = f"{person[0]}'s contact"
        cur.execute('''
            INSERT OR IGNORE INTO Contact (person_id, contact_name, relationship)
            VALUES (?, ?, ?)
        ''', (i, contact_name, 'sibling'))

        # Add emergency contact phone number
        contact_id = cur.lastrowid

        cur.execute('''
            INSERT OR IGNORE INTO Phone (owner_type, owner_id, phone_number, type)
            VALUES (?, ?, ?, ?)
        ''', ('contact', contact_id, f'+90312{i:06d}', 'emergency'))

    # === MEMBER ===
    cur.execute("INSERT OR IGNORE INTO Member (person_id, member_status) VALUES (?, ?)", (1, "active"))
    cur.execute("INSERT OR IGNORE INTO Member (person_id, member_status) VALUES (?, ?)", (2, "active"))
    cur.execute("INSERT OR IGNORE INTO Member (person_id, member_status) VALUES (?, ?)", (4, "inactive"))

    # === TRAINER ===
    cur.execute("INSERT OR IGNORE INTO Trainer (person_id, hire_date, trainer_status) VALUES (?, ?, ?)",
                (3, "2023-01-01", "active"))
    cur.execute("INSERT OR IGNORE INTO Trainer (person_id, hire_date, trainer_status) VALUES (?, ?, ?)",
                (5, "2022-05-15", "active"))

    # === SPECIALIZATION ===
    specializations = ["Yoga", "Pilates", "HIIT"]
    for s in specializations:
        cur.execute("INSERT OR IGNORE INTO Specialization (name) VALUES (?)", (s,))

    # === TRAINER_SPECIALIZATION ===
    cur.execute("INSERT OR IGNORE INTO Trainer_Specialization (trainer_id, specialization_id) VALUES (?, ?)", (1, 1))
    cur.execute("INSERT OR IGNORE INTO Trainer_Specialization (trainer_id, specialization_id) VALUES (?, ?)", (1, 2))
    cur.execute("INSERT OR IGNORE INTO Trainer_Specialization (trainer_id, specialization_id) VALUES (?, ?)", (2, 3))

    # === CLASS ===
    cur.execute("INSERT OR IGNORE INTO Class (class_name, description) VALUES (?, ?)",
                ("Yoga Basics", "Yoga for beginners"))
    cur.execute("INSERT OR IGNORE INTO Class (class_name, description) VALUES (?, ?)",
                ("Pilates Core", "Core strength and flexibility"))

    # === CLASS_SESSION ===
    cur.execute('''
        INSERT OR IGNORE INTO Class_Session (class_id, start_time, end_time, capacity, duration)
        VALUES (?, ?, ?, ?, ?)
    ''', (1, "2025-12-10 10:00", "2025-12-10 11:00", 10, 60))
    cur.execute('''
        INSERT OR IGNORE INTO Class_Session (class_id, start_time, end_time, capacity, duration)
        VALUES (?, ?, ?, ?, ?)
    ''', (2, "2025-12-11 14:00", "2025-12-11 15:00", 8, 60))

    # === MEMBERSHIP_TYPE ===
    cur.execute("INSERT OR IGNORE INTO Membership_Type (name, price) VALUES (?, ?)", ("Monthly", 300))
    cur.execute("INSERT OR IGNORE INTO Membership_Type (name, price) VALUES (?, ?)", ("Yearly", 3000))

    # === MEMBERSHIP ===
    cur.execute('''
        INSERT OR IGNORE INTO Membership (member_id, membership_type_id, is_active, start_date, end_date)
        VALUES (?, ?, ?, ?, ?)
    ''', (1, 1, 1, "2025-12-01", "2026-01-01"))

    # === PAYMENT ===
    cur.execute('''
        INSERT OR IGNORE INTO Payment (member_id, payment_date, method, amount)
        VALUES (?, ?, ?, ?)
    ''', (1, "2025-12-01", "credit_card", 300.0))

    # === CHECK-IN ===
    cur.execute('''
        INSERT OR IGNORE INTO Check_in (member_id, class_session_id, checkin_time, checkout_time)
        VALUES (?, ?, ?, ?)
    ''', (1, 1, "2025-12-10 09:50", "2025-12-10 11:00"))

    # === ATTENDS ===
    cur.execute("INSERT OR IGNORE INTO Attends (member_id, class_session_id) VALUES (?, ?)", (1, 1))

    # === TEACHES ===
    cur.execute("INSERT OR IGNORE INTO Teaches (trainer_id, class_session_id) VALUES (?, ?)", (1, 1))
    cur.execute("INSERT OR IGNORE INTO Teaches (trainer_id, class_session_id) VALUES (?, ?)", (2, 2))

    conn.commit()
    conn.close()

    print("Sample data inserted successfully.")
