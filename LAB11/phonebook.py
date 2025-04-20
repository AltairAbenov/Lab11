import psycopg2
import csv

conn = psycopg2.connect(
    dbname="DataBase",
    user="postgres",
    password="A2682772aa",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

def create_table():
    cur.execute("""
        CREATE TABLE IF NOT EXISTS PhoneBook (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100),
            phone VARCHAR(20)
        )
    """)
    conn.commit()
    print("Table created.")

def insert_from_csv(filename):
    with open(filename, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cur.execute("INSERT INTO PhoneBook (username, phone) VALUES (%s, %s)", row)
    conn.commit()
    print("Data from CSV inserted.")

def insert_from_console():
    username = input("Enter username: ")
    phone = input("Enter phone number: ")
    cur.execute("INSERT INTO PhoneBook (username, phone) VALUES (%s, %s)", (username, phone))
    conn.commit()
    print("Data inserted.")

def update_data():
    username = input("Enter username to update: ")
    new_phone = input("Enter new phone number: ")
    cur.execute("UPDATE PhoneBook SET phone = %s WHERE username = %s", (new_phone, username))
    conn.commit()
    print("Data updated.")

def query_data():
    filter_name = input("Enter name to filter by: ")
    cur.execute("SELECT * FROM PhoneBook WHERE username ILIKE %s", ('%' + filter_name + '%',))
    rows = cur.fetchall()
    for row in rows:
        print(row)

def delete_data():
    username = input("Enter username to delete: ")
    cur.execute("DELETE FROM PhoneBook WHERE username = %s", (username,))
    conn.commit()
    print("Data deleted.")

def search_by_pattern():
    pattern = input("Enter pattern (part of name or phone): ")
    cur.execute("SELECT * FROM search_pattern(%s);", (pattern,))
    for row in cur.fetchall():
        print(row)

def insert_or_update():
    username = input("Enter username: ")
    phone = input("Enter phone number: ")
    cur.execute("CALL insert_or_update_user(%s, %s);", (username, phone))
    conn.commit()
    print("User inserted or updated.")

def insert_many():
    users = []
    n = int(input("How many users to insert? "))
    for _ in range(n):
        username = input("Username: ")
        phone = input("Phone: ")
        users.append([username, phone])
    cur.execute("CALL insert_many(%s);", (users,))
    conn.commit()
    print("Bulk insert complete.")


def paginate():
    limit = int(input("Limit: "))
    offset = int(input("Offset: "))
    cur.execute("SELECT * FROM paginate(%s, %s);", (limit, offset))
    for row in cur.fetchall():
        print(row)

def delete_by_info():
    info = input("Enter username or phone to delete: ")
    cur.execute("CALL delete_by_info(%s);", (info,))
    conn.commit()
    print("User deleted.")

def menu():
    while True:
        print("\n=== Menu ===")
        print("1. Create table")
        print("2. Insert data from CSV")
        print("3. Insert data from console")
        print("4. Update data")
        print("5. Query data")
        print("6. Delete data")
        print("7. Search by pattern")
        print("8. Insert or update user")
        print("9. Insert many users")
        print("10. Paginate query")
        print("11. Delete by name or phone")
        print("0. Exit")

        choice = input("Choose an option: ")

        if choice == "1":
            create_table()
        elif choice == "2":
            insert_from_csv("contacts.csv")
        elif choice == "3":
            insert_from_console()
        elif choice == "4":
            update_data()
        elif choice == "5":
            query_data()
        elif choice == "6":
            delete_data()
        elif choice == "7":
            search_by_pattern()
        elif choice == "8":
            insert_or_update()
        elif choice == "9":
            insert_many()
        elif choice == "10":
            paginate()
        elif choice == "11":
            delete_by_info()
        elif choice == "0":
            break
        else:
            print("Invalid choice.")

    cur.close()
    conn.close()

if __name__ == "__main__":
    menu()
