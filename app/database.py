import sqlite3

DATABASE_NAME: str = "gym.db"

def create_tables() -> None:
    """
    Create all necessary database tables for the gym management system.
    Includes tables for persons, members, trainers, classes, memberships, and related entities.
    """
    conn : sqlite3.Connection = sqlite3.connect(DATABASE_NAME)
    cur : sqlite3.Cursor = conn.cursor()

    # Enable foreign key constraint to maintain referential integrity
    cur.execute('PRAGMA foreign_keys = ON;')


    # Initialization flag table
    # Used to track if sample data has been inserted to prevent redundant insertion
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Init_Flags (
            key TEXT PRIMARY KEY,
            value TEXT
        );
    ''')

    # PERSON
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Person (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name TEXT,
            last_name TEXT,
            birth_date TEXT,
            email TEXT,
            city TEXT,
            street TEXT,
            zip TEXT
        )
    ''')

    # PHONE 
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Phone(
            phone_id INTEGER PRIMARY KEY AUTOINCREMENT,
            owner_type TEXT CHECK(owner_type IN ('person', 'contact')),
            owner_id INTEGER,
            phone_number TEXT NOT NULL,
            type TEXT -- mobile, home, work, etc.
        )
    ''')

    # MEMBER
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Member (
            member_id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER UNIQUE,
            member_status TEXT,
            FOREIGN KEY (person_id) REFERENCES Person(id)
        )
    ''')

    # TRAINER
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Trainer (
            trainer_id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER UNIQUE,
            specialization TEXT,
            hire_date TEXT,
            trainer_status TEXT,
            FOREIGN KEY (person_id) REFERENCES Person(id)
        )
    ''')

    # SPECIALIZATION
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Specialization (
            specialization_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        )
    ''')

    # TRAINER SPECIALIZATION
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Trainer_Specialization (
            trainer_id INTEGER,
            specialization_id INTEGER,
            PRIMARY KEY (trainer_id, specialization_id),
            FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id),
            FOREIGN KEY (specialization_id) REFERENCES Specialization(specialization_id)
        )
    ''')

    # CONTACT
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Contact (
            contact_id INTEGER PRIMARY KEY AUTOINCREMENT,
            person_id INTEGER,
            contact_name TEXT,
            relationship TEXT,
            FOREIGN KEY (person_id) REFERENCES Person(id)
        )
    ''')

    # CLASS
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Class (
            class_id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_name TEXT,
            description TEXT
        )
    ''')

    # CLASS_SESSION
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Class_Session (
            class_session_id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER,
            start_time TEXT,
            end_time TEXT,
            capacity INTEGER,
            duration INTEGER,
            FOREIGN KEY (class_id) REFERENCES Class(class_id)
        )
    ''')

    # MEMBERSHIP_TYPE
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Membership_Type (
            membership_type_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL
        )
    ''')

    # MEMBERSHIP
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Membership (
            membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            membership_type_id INTEGER,
            is_active INTEGER,
            start_date TEXT,
            end_date TEXT,
            FOREIGN KEY (member_id) REFERENCES Member(member_id),
            FOREIGN KEY (membership_type_id) REFERENCES Membership_Type(membership_type_id)
        )
    ''')

    # PAYMENT
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Payment (
            payment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            payment_date TEXT,
            method TEXT,
            amount REAL,
            FOREIGN KEY (member_id) REFERENCES Member(member_id)
        )
    ''')

    # CHECK-IN
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Check_in (
            checkin_id INTEGER PRIMARY KEY AUTOINCREMENT,
            member_id INTEGER,
            class_session_id INTEGER,
            checkin_time TEXT,
            checkout_time TEXT,
            FOREIGN KEY (member_id) REFERENCES Member(member_id),
            FOREIGN KEY (class_session_id) REFERENCES Class_Session(class_session_id)
        )
    ''')

    # ATTENDS
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Attends (
            member_id INTEGER,
            class_session_id INTEGER,
            PRIMARY KEY (member_id, class_session_id),
            FOREIGN KEY (member_id) REFERENCES Member(member_id),
            FOREIGN KEY (class_session_id) REFERENCES Class_Session(class_session_id)
        )
    ''')

    # TEACHES
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Teaches (
            trainer_id INTEGER,
            class_session_id INTEGER,
            PRIMARY KEY (trainer_id, class_session_id),
            FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id),
            FOREIGN KEY (class_session_id) REFERENCES Class_Session(class_session_id)
        )
    ''')

    conn.commit()
    conn.close()
