import sqlite3
from database import DATABASE_NAME

def insert_sample_data():
    """
    Populates the database with extended sample data (approx. 10 records per table).
    Includes 20 Persons (10 Members, 10 Trainers) and related entities.
    Updated to handle single-value Phone numbers directly in Person and Contact tables.
    """
    conn = sqlite3.connect(DATABASE_NAME)
    cur = conn.cursor()

    # Enable foreign key constraints
    cur.execute("PRAGMA foreign_keys = ON;")

    # ==========================================
    # PERSON
    # ==========================================
    # We need enough people to have 10 Members and 10 Trainers.
    
    people = [
        ("Ali", "Yıldız", "1990-01-01", "ali@gmail.com", "Istanbul", "Mecidiyeköy", "34387"),   # 1
        ("Zeynep", "Arslan", "1988-02-14", "zeynep@gmail.com", "Ankara", "Kızılay", "06000"),   # 2
        ("Kemal", "Demir", "1995-03-30", "kemal@gmail.com", "Izmir", "Alsancak", "35000"),      # 3
        ("Emir", "Salaman", "1992-06-11", "emir@gmail.com", "Bursa", "Nilüfer", "16000"),       # 4
        ("Ece", "Aksoy", "1987-09-19", "ece@gmail.com", "Adana", "Çukurova", "01000"),          # 5
        ("Mert", "Öztürk", "1993-05-22", "mert@gmail.com", "Istanbul", "Kadıköy", "34700"),     # 6
        ("Seda", "Kaya", "1996-08-10", "seda@gmail.com", "Antalya", "Lara", "07100"),           # 7
        ("Kerem", "Şahin", "1991-11-05", "kerem@gmail.com", "Eskişehir", "Bağlar", "26000"),    # 8
        ("Leyla", "Çelik", "1998-04-15", "leyla@gmail.com", "Muğla", "Bodrum", "48400"),        # 9
        ("Baran", "Koç", "1985-12-30", "baran@gmail.com", "Gaziantep", "Şahinbey", "27000"),    # 10
        ("Pınar", "Tekin", "1994-07-07", "pinar@gmail.com", "Trabzon", "Ortahisar", "61000"),   # 11
        ("Volkan", "Yılmaz", "1989-09-25", "volkan@gmail.com", "Samsun", "Atakum", "55200"),    # 12
        ("Aslı", "Güneş", "1990-03-12", "asli@gmail.com", "Istanbul", "Beşiktaş", "34300"),     # 13
        ("Serkan", "Bulut", "1986-06-18", "serkan@gmail.com", "Ankara", "Çankaya", "06500"),    # 14
        ("Derya", "Tunç", "1992-01-20", "derya@gmail.com", "Izmir", "Bornova", "35040"),        # 15
        ("Tolga", "Erkin", "1988-10-05", "tolga@gmail.com", "Bursa", "Osmangazi", "16100"),     # 16
        ("Yasemin", "Kurt", "1995-02-28", "yasemin@gmail.com", "Mersin", "Yenişehir", "33100"), # 17
        ("Ozan", "Acar", "1991-07-14", "ozan@gmail.com", "Konya", "Selçuklu", "42000"),         # 18
        ("Berna", "Polat", "1997-11-11", "berna@gmail.com", "Kayseri", "Melikgazi", "38000"),   # 19
        ("Koray", "Avcı", "1984-04-04", "koray@gmail.com", "Denizli", "Pamukkale", "20000")     # 20
    ]

    for i, person in enumerate(people, start=1):
        # Generate fake phone number
        phone_num = f'+90555{i:07d}'
        
        # Insert Person
        cur.execute('''
            INSERT OR IGNORE INTO Person (first_name, last_name, birth_date, email, phone, city, street, zip)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (person[0], person[1], person[2], person[3], phone_num, person[4], person[5], person[6]))

        # Insert Contact
        contact_name = f"{person[0]}'s relative"
        contact_phone = f'+90500{i:07d}'
        
        cur.execute('''
            INSERT OR IGNORE INTO Contact (person_id, contact_name, relationship, phone)
            VALUES (?, ?, ?, ?)
        ''', (i, contact_name, 'family', contact_phone))

    # ==========================================
    # MEMBERSHIP TYPES
    # ==========================================
    m_types = [
        ("Monthly Standard", 500.0),
        ("Yearly Gold", 5000.0),
        ("Student Monthly", 350.0),
        ("Weekly Pass", 150.0),
        ("Daily Drop-in", 50.0),
        ("VIP Platinum", 10000.0),
        ("Corporate Plan", 4500.0),
        ("Off-Peak Access", 300.0),
        ("Senior Citizen", 250.0),
        ("Family Bundle", 8000.0)
    ]
    cur.executemany("INSERT OR IGNORE INTO Membership_Type (name, price) VALUES (?, ?)", m_types)

    # ==========================================
    # MEMBERS
    # ==========================================
    member_data = [
        (1, "active"), (2, "active"), (4, "inactive"),
        (6, "active"), (7, "pending"), (8, "active"),
        (9, "banned"), (10, "active"), (11, "active"), (12, "active")
    ]
    cur.executemany("INSERT OR IGNORE INTO Member (person_id, member_status) VALUES (?, ?)", member_data)

    # ==========================================
    # MEMBERSHIPS
    # ==========================================
    memberships = [
        (1, 1, 1, "2025-01-01", "2025-02-01"),
        (2, 2, 1, "2025-01-01", "2026-01-01"),
        (3, 3, 0, "2024-06-01", "2024-07-01"),
        (4, 1, 1, "2025-01-10", "2025-02-10"),
        (5, 4, 0, "2025-01-01", "2025-01-07"),
        (6, 6, 1, "2025-01-01", "2026-01-01"),
        (7, 5, 0, "2024-12-01", "2024-12-01"),
        (8, 7, 1, "2025-01-15", "2026-01-15"),
        (9, 3, 1, "2025-01-20", "2025-02-20"),
        (10, 2, 1, "2025-01-05", "2026-01-05")
    ]
    cur.executemany('''
        INSERT OR IGNORE INTO Membership (member_id, membership_type_id, is_active, start_date, end_date)
        VALUES (?, ?, ?, ?, ?)
    ''', memberships)

    # ==========================================
    # PAYMENTS
    # ==========================================
    payments = [
        (1, "2025-01-01", "credit_card", 500.0),
        (2, "2025-01-01", "credit_card", 5000.0),
        (3, "2024-06-01", "cash", 350.0),
        (4, "2025-01-10", "credit_card", 500.0),
        (5, "2025-01-01", "cash", 150.0),
        (6, "2025-01-01", "transfer", 10000.0),
        (7, "2024-12-01", "cash", 50.0),
        (8, "2025-01-15", "credit_card", 4500.0),
        (9, "2025-01-20", "cash", 350.0),
        (10, "2025-01-05", "credit_card", 5000.0)
    ]
    cur.executemany("INSERT OR IGNORE INTO Payment (member_id, payment_date, method, amount) VALUES (?, ?, ?, ?)", payments)

    # ==========================================
    # TRAINERS 
    # ==========================================
    trainers = [
        (3, "Yoga", "2023-01-01", "active"),
        (5, "Pilates", "2022-05-15", "active"),
        (13, "HIIT", "2023-06-10", "active"),
        (14, "Boxing", "2021-11-20", "active"),
        (15, "Swimming", "2024-02-01", "active"),
        (16, "BodyBuilding", "2020-08-15", "active"),
        (17, "Zumba", "2023-09-01", "on_leave"),
        (18, "CrossFit", "2022-03-12", "active"),
        (19, "Spinning", "2023-12-01", "active"),
        (20, "Kickboxing", "2021-07-22", "terminated")
    ]
    cur.executemany("INSERT OR IGNORE INTO Trainer (person_id, specialization, hire_date, trainer_status) VALUES (?, ?, ?, ?)", trainers)

    # ==========================================
    # SPECIALIZATIONS 
    # ==========================================
    specs = ["Yoga", "Pilates", "HIIT", "Boxing", "Swimming", "BodyBuilding", "Zumba", "CrossFit", "Spinning", "Kickboxing"]
    for s in specs:
        cur.execute("INSERT OR IGNORE INTO Specialization (name) VALUES (?)", (s,))

    # ==========================================
    # TRAINER_SPECIALIZATION
    # ==========================================
    t_specs = [(i, i) for i in range(1, 11)] 
    cur.executemany("INSERT OR IGNORE INTO Trainer_Specialization (trainer_id, specialization_id) VALUES (?, ?)", t_specs)

    # ==========================================
    # CLASSES
    # ==========================================
    classes = [
        ("Morning Yoga", "Gentle yoga for start"),
        ("Core Pilates", "Strengthen your core"),
        ("HIIT Burn", "High intensity cardio"),
        ("Fight Club", "Boxing techniques"),
        ("Aqua Man", "Swimming basics"),
        ("Iron Pump", "Weight lifting class"),
        ("Dance Party", "Zumba dance mix"),
        ("WOD Extreme", "CrossFit daily workout"),
        ("Spin City", "Indoor cycling cardio"),
        ("Kick Power", "Kickboxing advanced")
    ]
    cur.executemany("INSERT OR IGNORE INTO Class (class_name, description) VALUES (?, ?)", classes)

    # ==========================================
    # CLASS_SESSIONS
    # ==========================================
    sessions = [
        (1, "2025-12-10 09:00", "2025-12-10 10:00", 15, 60),
        (2, "2025-12-10 10:30", "2025-12-10 11:30", 10, 60),
        (3, "2025-12-10 12:00", "2025-12-10 13:00", 20, 60),
        (4, "2025-12-11 09:00", "2025-12-11 10:00", 8, 60),
        (5, "2025-12-11 14:00", "2025-12-11 15:00", 12, 60),
        (6, "2025-12-12 18:00", "2025-12-12 19:00", 25, 60),
        (7, "2025-12-13 19:00", "2025-12-13 20:00", 30, 60),
        (8, "2025-12-14 08:00", "2025-12-14 09:00", 10, 60),
        (9, "2025-12-14 10:00", "2025-12-14 11:00", 15, 60),
        (10, "2025-12-15 17:00", "2025-12-15 18:00", 12, 60)
    ]
    cur.executemany('''
        INSERT OR IGNORE INTO Class_Session (class_id, start_time, end_time, capacity, duration)
        VALUES (?, ?, ?, ?, ?)
    ''', sessions)

    # ==========================================
    # TEACHES 
    # ==========================================
    teaches_data = [(i, i) for i in range(1, 11)]
    cur.executemany("INSERT OR IGNORE INTO Teaches (trainer_id, class_session_id) VALUES (?, ?)", teaches_data)

    # ==========================================
    # ATTENDS
    # ==========================================
    attends_data = [(i, i) for i in range(1, 11)]
    cur.executemany("INSERT OR IGNORE INTO Attends (member_id, class_session_id) VALUES (?, ?)", attends_data)

    # ==========================================
    # CHECK-IN
    # ==========================================
    checkins = []
    for i in range(1, 11):
        s_date = sessions[i-1][1].split(" ")[0]
        s_time = sessions[i-1][1].split(" ")[1]
        c_in = f"{s_date} {s_time}"
        c_out = f"{s_date} {sessions[i-1][2].split(' ')[1]}"
        checkins.append((i, i, c_in, c_out))

    cur.executemany('''
        INSERT OR IGNORE INTO Check_in (member_id, class_session_id, checkin_time, checkout_time)
        VALUES (?, ?, ?, ?)
    ''', checkins)

    conn.commit()
    conn.close()