import psycopg2
from psycopg2 import sql

#DB details will live here
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "A3Q1",
    "user": "postgres",
    "password": "password"
}

def connect_to_db(): #connect to the db and return a connection object
    try:
        return psycopg2.connect(**DB_CONFIG)
    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")

def getAllStudents(): #get all students from the database
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT student_id, first_name, last_name, email, enrollment_date FROM students ORDER BY student_id;")
            rows = cur.fetchall()
            print("\n--- All Students ---")
            for row in rows:
                print(f"ID: {row[0]} | {row[1]} {row[2]} | {row[3]} | {row[4]}")
            if not rows:
                print("(no students found)")
    finally:
        conn.close()

def addStudent(first_name, last_name, email, enrollment_date):  #insert a new student into the students table
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO students (first_name, last_name, email, enrollment_date)
                VALUES (%s, %s, %s, %s)
                RETURNING student_id;
                """,
                (first_name, last_name, email, enrollment_date),
            )
            new_id = cur.fetchone()[0]
            conn.commit()
            print(f"Added student with ID {new_id}: {first_name} {last_name}")
    except Exception as e:
        conn.rollback()
        print(f"Error adding student: {e}")
    finally:
        conn.close()

def updateStudentEmail(student_id, new_email): #update the email for the student with the given student_id
    conn = connect_to_db()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE students SET email = %s WHERE student_id = %s;",
                (new_email, student_id),
            )
            if cur.rowcount == 0:
                print(f"No student found with ID {student_id}")
            else:
                conn.commit()
                print(f"Updated email for student {student_id} to {new_email}")
    except Exception as e:
        conn.rollback()
        print(f"Error updating email: {e}")
    finally:
        conn.close()



#here is where I test stuff
#addStudent("John", "Doe", "john2.doe@example.com", "2023-09-01")
updateStudentEmail(1, "bob.doe@example.com")
getAllStudents()
