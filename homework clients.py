import psycopg2


def create_db(conn):
    sql = """create table if not exists clients(
 client_id serial primary key,
 first_name varchar(255) not null,
 last_name varchar(255),
 email varchar(255)
);

create table if not exists client_phones(
 phone_id serial primary key,
 client_id int references clients(client_id),
 phone varchar(25) not null
);"""
    cursor = conn.cursor()
    cursor.execute(sql)
    cursor.close()


def add_client(conn, first_name, last_name, email, phone=None):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO clients(first_name, last_name, email) VALUES(%s, %s, %s) RETURNING client_id",
                   (first_name, last_name, email))
    client_id = cursor.fetchone()[0]
    cursor.close()

    if phone:
        add_phone(conn, client_id, phone)


def add_phone(conn, client_id, phone):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO client_phones(client_id, phone) VALUES(%s, %s)", (client_id, phone))
    cursor.close()


def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    if first_name:
        cursor = conn.cursor()
        cursor.execute("UPDATE clients set first_name=%s where client_id=%s", (first_name, client_id))
        cursor.close()

    if last_name:
        cursor = conn.cursor()
        cursor.execute("UPDATE clients set last_name=%s where client_id=%s", (last_name, client_id))
        cursor.close()

    if email:
        cursor = conn.cursor()
        cursor.execute("UPDATE clients set email=%s where client_id=%s", (email, client_id))
        cursor.close()


def delete_phone(conn, client_id, phone):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM client_phones WHERE client_id=%s AND phone=%s", (client_id, phone))
    cursor.close()


def delete_client(conn, client_id):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM client_phones WHERE client_id=%s", (client_id,))
    cursor.close()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM clients WHERE client_id=%s", (client_id,))
    cursor.close()


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    sql = "select client_id from clients where 1=1"

    if first_name:
        sql += f" and first_name = '{first_name}'"
    if last_name:
        sql += f" and last_name = '{last_name}'"
    if email:
        sql += f" and email = '{email}'"
    if phone:
        sql += f" and client_id in (select client_id from client_phones where phone = '{phone}')"

    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    return rows


with psycopg2.connect(database="test", user="postgres", password="postgres") as conn:
    create_db(conn)
    add_client(conn, "John", "Smith", "js@mail.ru")
    add_client(conn, "Johnny", "Smitson", "jsmit@mail.ru", "89501234567")
    add_phone(conn, 1, "89619876543")
    change_client(conn, 1, "David", "Clark", "david@mail.ru")
    delete_phone(conn, 2, "89501234567")
    delete_client(conn, 2)
    rows = find_client(conn, "Johnny", "Smitson", "jsmit@mail.ru", "89501234567")
    print(rows)
