import psycopg2

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
        return None

def getAllStudents(): #get all students from the database
    conn = connect_to_db()
    if conn is None:
        return
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
    if conn is None:
        return
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
    if conn is None:
        return
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

def deleteStudent(student_id): #delete the student with the given student_id
    conn = connect_to_db()
    if conn is None:
        return
    try:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM students WHERE student_id = %s;",
                (student_id,),
            )
            if cur.rowcount == 0:
                print(f"No student found with ID {student_id}")
            else:
                conn.commit()
                print(f"Deleted student with ID {student_id}")
    except Exception as e:
        conn.rollback()
        print(f"Error deleting student: {e}")
    finally:
        conn.close()

def print_menu():
    print("\n===== Student Management =====")
    print("1. Get all students")
    print("2. Add a student")
    print("3. Update a student's email")
    print("4. Delete a student")
    print("5. Exit")

def main():
    while True:
        print_menu()
        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            getAllStudents()

        elif choice == "2":
            first_name = input("First name: ").strip()
            last_name = input("Last name: ").strip()
            email = input("Email: ").strip()
            enrollment_date = input("Enrollment date (YYYY-MM-DD): ").strip()
            addStudent(first_name, last_name, email, enrollment_date)

        elif choice == "3":
            try:
                student_id = int(input("Student ID: ").strip())
            except ValueError:
                print("Student ID must be a number.")
                continue
            new_email = input("New email: ").strip()
            updateStudentEmail(student_id, new_email)

        elif choice == "4":
            try:
                student_id = int(input("Student ID: ").strip())
            except ValueError:
                print("Student ID must be a number.")
                continue
            deleteStudent(student_id)

        elif choice == "5":
            print("Goodbye!")
            break

        else:
            print("Invalid choice. Please enter 1-5.")

if __name__ == "__main__":
    main()
