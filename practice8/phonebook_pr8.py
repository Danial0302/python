import psycopg2
from config import parametrs

# ------------------------ CONNECTION ------------------------
def get_con():
    return psycopg2.connect(
        host=parametrs['host'],
        database=parametrs['database'],
        user=parametrs['user'],
        password=parametrs['password']
    )

# ------------------------ EXECUTE SQL FILE ------------------------
def execute_sql_file(file_sql, connection):
    with open(file_sql, "r") as file:
        sql_commands = file.read()
    with connection.cursor() as cur:
        cur.execute(sql_commands)
    connection.commit()

# ------------------------ CREATE TABLE ------------------------
def create_table():
    with get_con() as conn:
        with conn.cursor() as cur:
            cur.execute('''
                CREATE TABLE IF NOT EXISTS phonebook_pr8(
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(200) UNIQUE,
                    phone VARCHAR(20)
                );
            ''')
            conn.commit()

# ------------------------ SEE ALL CONTACTS ------------------------
def see_phonebook_pr8():
    with get_con() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM phonebook_pr8")
            rows = cur.fetchall()
            if not rows:
                print("Phonebook is empty.")
            else:
                for row in rows:
                    print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
        conn.commit()

# ------------------------ FIND CONTACT ------------------------
def find_contact(text):
    with get_con() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM find_name_or_phone(%s)", (text,))
            rows = cur.fetchall()
            if rows:
                for row in rows:
                    print(f"Name: {row[0]}, Phone: {row[1]}")
            else:
                print("No contacts found.")

# ------------------------ UPSERT USER ------------------------
def upsert_user(name, phone):
    with get_con() as conn:
        with conn.cursor() as cur:
            # if you use function from functions.sql
            cur.execute("SELECT upsert_contact(%s, %s)", (name, phone))
            conn.commit()
            print("Upserted User successfully.")

# ------------------------ ADD MANY CONTACTS ------------------------
def add_many_contacts():
    names = ['Dias', 'Maks', 'Sergey', 'Aigul', 'Bagdat']
    phones = ['87071112233', '87014445566', '123', '87470009988', '8707aaa1111']
    with get_con() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM insert_many_users(%s::TEXT[], %s::TEXT[])",
                (names, phones)
            )
            invalid_data = cur.fetchall()
            conn.commit()
            if invalid_data:
                print("Invalid entries found:")
                for row in invalid_data:
                    print(f"Name: {row[0]}, Phone: {row[1]}")
            else:
                print("All users added successfully.")

# ------------------------ SEE CONTACTS BY PAGE ------------------------
def see_contact_pages():
    limit = 7
    try:
        page = int(input("Enter page number (1-7): "))
        if page < 1 or page > 7:
            print("Invalid page number")
            return
    except ValueError:
        print("Please enter a valid number")
        return

    offset = (page - 1) * limit
    with get_con() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM get_contact_pages(%s, %s)", (limit, offset))
            rows = cur.fetchall()
            if not rows:
                print("This page has no information.")
            else:
                print(f"----- Contacts on page {page} -----")
                for row in rows:
                    print(f"Name: {row[0]}, Phone: {row[1]}")

# ------------------------ DELETE CONTACT ------------------------
def del_contact():
    del_user = input("Enter name or phone to delete: ")
    with get_con() as conn:
        with conn.cursor() as cur:
            # if you use function from functions.sql
            cur.execute("SELECT delete3_contact(%s)", (del_user,))
            conn.commit()
            print("Deleted contact successfully.")

# ------------------------ MENU ------------------------
def menu():
    create_table()
    conn = get_con()
    try:
        execute_sql_file("functions.sql", conn)
        # execute_sql_file("procedure.sql", conn)  # commented out to avoid routine kind conflict
    except Exception as e:
        print(f"Error executing SQL files: {e}")

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Search | 2. Upsert | 3. Add Many | 4. Pages | 5. Delete | 6. See All | 0. Exit")
        choice = input("Select: ")
        if choice == '1':
            find_contact(input("Search term: "))
        elif choice == '2':
            upsert_user(input("Name: "), input("Phone: "))
        elif choice == '3':
            add_many_contacts()
        elif choice == '4':
            see_contact_pages()
        elif choice == '5':
            del_contact()
        elif choice == '6':
            see_phonebook_pr8()
        elif choice == '0':
            break
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":
    menu()

