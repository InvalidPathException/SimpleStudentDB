import psycopg
from prettytable import PrettyTable
conn = None  # must use global variable to replicate the signatures
user = "postgres"  # you can change the default settings here
host = "localhost"
port = "5432"


'''
    This function is the main function of the program, it repeatedly displays the menu and processes the user's choice
'''
def main():
    global conn
    conn = connect()
    while True:
        printMenu()
        choice = input("Enter the number of your choice: ")
        if choice == "1":
            getAllStudents()
        elif choice == "2":
            first_name = input("Enter the student's first name: ")
            last_name = input("Enter the student's last name: ")
            email = input("Enter the student's email: ")
            enrollment_date = input("Enter the student's enrollment date (YYYY-MM-DD): ")
            addStudent(first_name, last_name, email, enrollment_date)
        elif choice == "3":
            student_id = input("Enter the student's ID: ")
            new_email = input("Enter the student's new email: ")
            updateStudentEmail(student_id, new_email)
        elif choice == "4":
            student_id = input("Enter the student's ID: ")
            deleteStudent(student_id)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.\n")
    conn.close()


def printWelcome():
    print("Welcome to SimpleStudentDatabaseManager!")
    print("Before continuing, please make sure that:")
    print("1. You have a local PostgreSQL server running on the default port (5432)")
    print("2. A database is already created using the provided DDL script")
    print("3. This program uses the 'postgres' user to connect to the database to ensure you have the permissions")


def printMenu():
    print("What would you like to do?")
    print("1. Display all records from the students table")
    print("2. Add a student")
    print("3. Update a student's E-mail")
    print("4. Delete a student")
    print("5. Exit")


'''
    This function connects to the database using the user's input for the database name and password
'''
def connect():
    global conn, user, host, port
    while True:
        dbname = input("Please enter the name of the database: ")
        password = input("Please enter the password for the 'postgres' user: ")
        try:
            conn = psycopg.connect(f"dbname={dbname} user={user} password={password} host={host} port={port}")
            print("Connection successful!")
            return conn
        except Exception as e:
            print(f"Error: {e}")


'''
    This function retrieves all students from the students table and displays them in a table format
'''
def getAllStudents():
    global conn
    if conn is None:
        print("Please connect to the database first.")
        return
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM students ORDER BY student_id")
        rows = cur.fetchall()

        table = PrettyTable()  # Creating a PrettyTable
        table.field_names = [desc[0] for desc in cur.description]
        print(f"Here are the {cur.rowcount} rows in the database:")

        for row in rows:
            table.add_row([row[0], row[1], row[2], row[3], row[4]])  # Add rows to the table
        print(table)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        print("")
        cur.close()  # Ensure the cursor is closed after operation


'''
    This function adds a student to the students table
    The student's first name, last name, email, and enrollment date are specified as parameters
'''
def addStudent(first_name, last_name, email, enrollment_date):
    global conn
    if conn is None:
        print("Please connect to the database first.")
        return
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO students (first_name, last_name, email, enrollment_date) VALUES (%s, %s, %s, %s)", (first_name, last_name, email, enrollment_date))
        conn.commit()  # commit the transaction
        print("Student added successfully!")
    except Exception as e:
        conn.rollback()  # rollback the transaction if an error occurs
        print(f"Error: {e}")
    finally:
        print("")  # print an empty line and close the cursor
        cur.close()


'''
    This function updates the email of a student with the specified student_id
    If the student does not exist, no changes are made to the database
'''
def updateStudentEmail(student_id, new_email):
    global conn
    if conn is None:
        print("Please connect to the database first.")
        return
    try:
        cur = conn.cursor()
        cur.execute("UPDATE students SET email = %s WHERE student_id = %s", (new_email, student_id))
        if cur.rowcount == 0:  # the student with the specified ID does not exist (no changes were made)
            print("No student found with the specified ID. No changes were made.")
        else:  # the student with the specified ID was successfully updated
            conn.commit()  # commit the transaction
            print("Student email updated successfully!")
    except Exception as e:
        conn.rollback()  # rollback the transaction if an error occurs
        print(f"Error: {e}")
    finally:
        print("")  # print an empty line and close the cursor
        cur.close()


'''
    This function deletes a student from the students table with the specified student_id
    If the student does not exist, no changes are made to the database
'''
def deleteStudent(student_id):
    global conn
    if conn is None:
        print("Please connect to the database first.")
        return
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM students WHERE student_id = %s", (student_id,))
        if cur.rowcount == 0:  # the student with the specified ID does not exist (no changes were made)
            print("No student found with the specified ID. No changes were made.")
        else:  # the student with the specified ID was successfully deleted
            conn.commit()  # commit the transaction
            print("Student email updated successfully!")
    except Exception as e:
        conn.rollback()  # rollback the transaction if an error occurs
        print(f"Error: {e}")
    finally:
        print("")  # print an empty line and close the cursor
        cur.close()


if __name__ == "__main__":
    main()
