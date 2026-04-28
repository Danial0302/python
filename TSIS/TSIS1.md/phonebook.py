from connect import get_con
import json
import csv
import os


# ---------------- PRINT ----------------
def print_contacts(rows):
    print("\n{:<12} {:<25} {:<12} {:<10} {:<15} {:<10}".format(
        "Name","Email","Birthday","Group","Phone","Type"
    ))
    print("-"*90)

    for r in rows:
        print("{:<12} {:<25} {:<12} {:<10} {:<15} {:<10}".format(
            str(r[0]), str(r[1]), str(r[2]),
            str(r[3]), str(r[4]), str(r[5])
        ))


# ---------------- VIEW PAGES ----------------
def view_contacts_pages():
    page = 1
    limit = 5

    while True:
        offset = (page-1)*limit

        with get_con() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                SELECT c.name,c.email,c.birthday,g.name,p.phone,p.type
                FROM contacts c
                LEFT JOIN groups g ON c.group_id=g.id
                LEFT JOIN phones p ON c.id=p.contact_id
                ORDER BY c.name
                LIMIT %s OFFSET %s
                """,(limit,offset))

                rows = cur.fetchall()

        print(f"\nPage {page}")
        if rows:
            print_contacts(rows)
        else:
            print("No data.")

        cmd=input("\n[n] next [p] prev [q] back → ").lower()

        if cmd=="n" and rows:
            page+=1
        elif cmd=="p" and page>1:
            page-=1
        elif cmd=="q":
            break


# ---------------- SEARCH ----------------
def search_filter_sort():
    q=input("Search: ")
    group=input("Group: ")
    sort=input("Sort (name/birthday/created_at): ")

    if sort not in ["name","birthday","created_at"]:
        sort="name"

    sql="""
    SELECT c.name,c.email,c.birthday,g.name,p.phone,p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id=g.id
    LEFT JOIN phones p ON c.id=p.contact_id
    WHERE 1=1
    """

    params=[]

    if q:
        sql+=" AND (c.name ILIKE %s OR c.email ILIKE %s OR p.phone ILIKE %s)"
        params+=[f"%{q}%",f"%{q}%",f"%{q}%"]

    if group:
        sql+=" AND g.name ILIKE %s"
        params.append(f"%{group}%")

    sql+=f" ORDER BY c.{sort}"

    with get_con() as conn:
        with conn.cursor() as cur:
            cur.execute(sql,params)
            print_contacts(cur.fetchall())


# ---------------- ADD PHONE ----------------
def add_phone_console():
    name=input("Name: ")
    phone=input("Phone: ")
    t=input("Type(home/work/mobile): ")

    with get_con() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL add_phone(%s,%s,%s)",(name,phone,t))


# ---------------- MOVE GROUP ----------------
def move_group_console():
    name=input("Name: ")
    group=input("New group: ")

    with get_con() as conn:
        with conn.cursor() as cur:
            cur.execute("CALL move_to_group(%s,%s)",(name,group))


# ---------------- EXPORT JSON ----------------
def export_json():
    data=[]

    with get_con() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            SELECT c.id,c.name,c.email,c.birthday,g.name
            FROM contacts c
            LEFT JOIN groups g ON c.group_id=g.id
            """)

            for cid,name,email,birthday,group in cur.fetchall():

                cur.execute("SELECT phone,type FROM phones WHERE contact_id=%s",(cid,))
                phones=cur.fetchall()

                data.append({
                    "name":name,
                    "email":email,
                    "birthday":str(birthday),
                    "group":group,
                    "phones":[{"phone":p[0],"type":p[1]} for p in phones]
                })

    with open("contacts.json","w") as f:
        json.dump(data,f,indent=4)

    print("Exported to contacts.json")


# ---------------- IMPORT CSV (FINAL FIX) ----------------
def import_csv(filename="contacts.csv"):

    base_path = os.path.dirname(__file__)
    full_path = os.path.join(base_path, filename)

    with open(full_path,"r",encoding="utf-8") as f:
        reader=csv.DictReader(f)

        with get_con() as conn:
            with conn.cursor() as cur:

                for row in reader:

                    # GROUP
                    cur.execute("""
                    INSERT INTO groups(name)
                    VALUES (%s)
                    ON CONFLICT(name) DO NOTHING
                    """,(row["group"],))

                    cur.execute("SELECT id FROM groups WHERE name=%s",(row["group"],))
                    gid=cur.fetchone()[0]

                    # CONTACT (UPDATE IF EXISTS)
                    cur.execute("""
                    INSERT INTO contacts(name,email,birthday,group_id)
                    VALUES (%s,%s,%s,%s)
                    ON CONFLICT (name) DO UPDATE
                    SET email=EXCLUDED.email,
                        birthday=EXCLUDED.birthday,
                        group_id=EXCLUDED.group_id
                    RETURNING id
                    """,(
                        row["name"],
                        row["email"],
                        row["birthday"],
                        gid
                    ))

                    cid=cur.fetchone()[0]

                    # PHONE
                    cur.execute("""
                    INSERT INTO phones(contact_id,phone,type)
                    VALUES (%s,%s,%s)
                    """,(
                        cid,
                        row["phone"],
                        row["type"]
                    ))

    print("CSV imported successfully.")


# ---------------- DB SEARCH FUNCTION ----------------
def search_function():
    q=input("Search all fields: ")

    with get_con() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM search_contacts(%s)",(q,))
            print_contacts(cur.fetchall())


# ---------------- MENU ----------------
def menu():
    while True:
        print("""
=============================
PHONEBOOK APP
=============================
1. View contacts
2. Search / Filter
3. Add phone
4. Move group
5. Export JSON
6. Import CSV
7. DB search function
0. Exit
=============================
""")

        ch=input("Choose → ")

        if ch=="1": view_contacts_pages()
        elif ch=="2": search_filter_sort()
        elif ch=="3": add_phone_console()
        elif ch=="4": move_group_console()
        elif ch=="5": export_json()
        elif ch=="6": import_csv()
        elif ch=="7": search_function()
        elif ch=="0": break


if __name__=="__main__":
    menu()