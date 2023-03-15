import psycopg2


def create_db(conn):
    sql = """
    create table if not exists clients(
        client_id serial primary key,
        first_name varchar(255) not null,
        last_name varchar(255),
        email varchar(255) not null unique
    );
    create table if not exists client_phones(
        phone_id serial primary key,
        client_id int not null references clients(client_id) on delete cascade,
        phone varchar(25) not null unique
    );
    """
    with conn.cursor() as curs:
        curs.execute(sql)


def get_client_id(conn, email):
    with conn.cursor() as curs:
        curs.execute("select client_id from clients where email = %s", (email,))
        row = curs.fetchone()
        if row is not None:
            return row[0]
        else:
            return None


def client_exists(conn, client_id):
    with conn.cursor() as curs:
        curs.execute("select client_id from clients where client_id = %s", (client_id,))
        return curs.fetchone() is not None


def add_client(conn, first_name, last_name, email, phone=None):
    with conn.cursor() as curs:
        client_id = get_client_id(conn, email)
        if client_id:
            return "Error: client already exists"
        curs.execute(
            """
            insert into clients(first_name, last_name, email)
            values(%s, %s, %s) returning client_id
            """,
            (first_name, last_name, email))
        client_id = curs.fetchone()[0]
        if phone:
            res = add_phone(conn, client_id, phone)
            if res != "OK":
                conn.rollback()
                return f"Error: {res}"
        conn.commit()
        return "OK"


def add_phone(conn, client_id, phone):
    if not client_exists(conn, client_id):
        return "Error: client does not exist"
    with conn.cursor() as curs:
        curs.execute(
            """
            select phone_id from client_phones where phone = %s
            """, (phone,))
        if curs.fetchone():
            return "Error: phone already exists"
        curs.execute(
            """
            insert into client_phones(client_id, phone) values(%s, %s)
            """, (client_id, phone))
        conn.commit()
        return "OK"


def change_client(conn, client_id, first_name=None, last_name=None, email=None):
    if not client_exists(conn, client_id):
        return "Error: client does not exist"
    if first_name:
        with conn.cursor() as curs:
            curs.execute(
                """
                update clients set first_name=%s where client_id=%s
                """, (first_name, client_id))
    if last_name:
        with conn.cursor() as curs:
            curs.execute(
                """
                update clients set last_name=%s where client_id=%s
                """, (last_name, client_id))
    if email:
        with conn.cursor() as curs:
            curs.execute(
                """
                update clients set email=%s where client_id=%s
                """, (email, client_id))
    conn.commit()
    return "OK"


def delete_phone(conn, client_id, phone):
    if not client_exists(conn, client_id):
        return "Error: client does not exist"
    with conn.cursor() as curs:
        curs.execute(
            """
            delete from client_phones where client_id=%s and phone=%s
            """, (client_id, phone))
        conn.commit()
        return "OK"


def delete_client(conn, client_id):
    if not client_exists(conn, client_id):
        return "Error: client does not exist"
    with conn.cursor() as curs:
        curs.execute(
            """
            delete from clients where client_id=%s
            """, (client_id,))
        conn.commit()
        return "OK"


def find_client(conn, first_name=None, last_name=None, email=None, phone=None):
    if first_name is None:
        first_name = '%'
    if last_name is None:
        last_name = '%'
    if email is None:
        email = '%'
    param_list = [first_name, last_name, email]
    sql_phone = ''
    if phone is None:
        phone = '%'
    else:
        sql_phone = " and phone = %s::text"
        param_list.append(phone)
    with conn.cursor() as curs:
        sql = f"""
            select c.client_id, c.first_name, c.last_name, c.email,
            case when array_agg(p.phone) = '{{Null}}' then array[]::text[]
                 else array_agg(p.phone)
            end as phones
            from clients c
            left join client_phones p
            on c.client_id = p.client_id
            where c.first_name like %s
            and c.last_name like %s
            and c.email like %s
            {sql_phone}
            group by c.client_id, c.first_name, c.last_name, c.email
            """
        curs.execute(sql, param_list)
        return curs.fetchall()


with psycopg2.connect(database="test", user="postgres", password="postgres") as conn:
    create_db(conn)
    add_client(conn, "John", "Smith", "js@mail.ru")
    add_client(conn, "Johnny", "Smitson", "jsmit@mail.ru", "89501234567")
    add_phone(conn, 1, "89619876543")
    add_phone(conn, 1, "81234567890")
    change_client(conn, 1, "David", "Clark", "david@mail.ru")
    delete_phone(conn, 2, "89501234567")
    delete_client(conn, 2)
    print(find_client(conn, "David"))
    print(find_client(conn, "David", "Clark", "david@mail.ru", "89619876543"))
    print(find_client(conn, None, None, None, "89619876543"))
