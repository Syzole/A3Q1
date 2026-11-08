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



#here is where I test stuff

getAllStudents()
