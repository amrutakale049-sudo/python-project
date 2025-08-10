import sqlite3
from datetime import datetime

# Connect to SQLite database (or create it)
conn = sqlite3.connect("hospital.db")
cursor = conn.cursor()

# Create tables
cursor.execute("""
CREATE TABLE IF NOT EXISTS doctors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    specialization TEXT NOT NULL
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS patients (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    age INTEGER,
    gender TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS appointments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    patient_id INTEGER,
    doctor_id INTEGER,
    date TEXT,
    time TEXT,
    FOREIGN KEY(patient_id) REFERENCES patients(id),
    FOREIGN KEY(doctor_id) REFERENCES doctors(id),
    UNIQUE(doctor_id, date, time) -- prevent double booking
)
""")

conn.commit()

# ------------------ Functionalities ------------------

def add_doctor():
    name = input("Enter doctor's name: ")
    specialization = input("Enter specialization: ")
    cursor.execute("INSERT INTO doctors (name, specialization) VALUES (?, ?)", (name, specialization))
    conn.commit()
    print("Doctor added successfully.\n")

def register_patient():
    name = input("Enter patient's name: ")
    age = input("Enter age: ")
    gender = input("Enter gender: ")
    cursor.execute("INSERT INTO patients (name, age, gender) VALUES (?, ?, ?)", (name, age, gender))
    conn.commit()
    print("Patient registered successfully.\n")

def list_doctors():
    cursor.execute("SELECT * FROM doctors")
    doctors = cursor.fetchall()
    print("\n--- Available Doctors ---")
    for doc in doctors:
        print(f"ID: {doc[0]}, Name: {doc[1]}, Specialization: {doc[2]}")
    print()

def book_appointment():
    list_doctors()
    patient_id = input("Enter your patient ID: ")
    doctor_id = input("Enter doctor ID to book: ")
    date = input("Enter appointment date (YYYY-MM-DD): ")
    time = input("Enter time (HH:MM): ")

    try:
        datetime.strptime(date, "%Y-%m-%d")
        datetime.strptime(time, "%H:%M")
    except ValueError:
        print("Invalid date or time format.\n")
        return

    try:
        cursor.execute("""
            INSERT INTO appointments (patient_id, doctor_id, date, time)
            VALUES (?, ?, ?, ?)
        """, (patient_id, doctor_id, date, time))
        conn.commit()
        print("Appointment booked successfully.\n")
    except sqlite3.IntegrityError:
        print("The selected time slot is already booked. Please choose another time.\n")

def view_appointments():
    cursor.execute("""
    SELECT a.id, p.name, d.name, d.specialization, a.date, a.time
    FROM appointments a
    JOIN patients p ON a.patient_id = p.id
    JOIN doctors d ON a.doctor_id = d.id
    ORDER BY a.date, a.time
    """)
    appointments = cursor.fetchall()
    print("\n--- All Appointments ---")
    for appt in appointments:
        print(f"Appointment ID: {appt[0]}, Patient: {appt[1]}, Doctor: {appt[2]} ({appt[3]}), Date: {appt[4]}, Time: {appt[5]}")
    print()

# ------------------ Menu ------------------

def main():
    while True:
        print("=== Hospital Appointment System ===")
        print("1. Add Doctor")
        print("2. Register Patient")
        print("3. Book Appointment")
        print("4. View Appointments")
        print("5. Exit")
        choice = input("Select an option (1-5): ")

        if choice == '1':
            add_doctor()
        elif choice == '2':
            register_patient()
        elif choice == '3':
            book_appointment()
        elif choice == '4':
            view_appointments()
        elif choice == '5':
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Try again.\n")

if __name__ == "__main__":
    main()
