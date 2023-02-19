import psycopg2
# import sqlalchemy
#
# DSN = 'postgresql://postgres:12345@localhost:5432/diplomaneto'
# engine = sqlalchemy.create_engine(DSN)
# connection = engine.connect()


def create_db():
    initial_connection = psycopg2.connect(
        database='diplomaneto',
        user='postgres',
        password='12345',
        host='localhost',
        port='5432'
    )
    initial_connection.close()

connection = psycopg2.connect(
        database='diplomaneto',
        user='postgres',
        password='12345',
        host='localhost',
        port='5432'
    )

connection.autocommit = True

def create_users():
    with connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            vk_id INTEGER(9) NOT NULL,
            first_name VARCHAR(20) NOT NULL,
            last_name VARCHAR(20),
            vk_link VARCHAR(30) NOT NULL
            '''
         )
        print("[INFO] Table USERS was created.")


def create_dating_users():
    with connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS dating_users(
            id SERIAL PRIMARY KEY,
            du_vk_id INTEGER(9) NOT NULL,
            user_id INTEGER(9) NOT NULL
            );
        ''')


def create_compilation():
    with connection.cursor() as cursor:
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS compilation (
            user_id INTEGER(9) NOT NULL REFERENCES users(id),
            d_user_id INTEGER(9) NOT NULL REFERENCES dating_users(user_id),
            CONSTRAINT pk PRIMARY KEY (user_id, d_user_id
            );
        ''')


def insert_users(vk_id, first_name, last_name, vk_link):
    with connection.cursor() as cursor:
        cursor.execute('''
            INSERT INTO users(vk_id, first_name, last_name, vk_link) 
            VALUES
                ({vk_id}, {first_name}, {last_name}, {vk_link}
            );
        ''')


def insert_dating_users(du_vk_id, user_id):
    with connection.cursor() as cursor:
        cursor.execute('''
            INSERT INTO dating_users(du_vk_id, user_id) 
            VALUES
                ({du_vk_id}, {user_id}
            );
        ''')


def select(offset):
    with connection.cursor() as cursor:
        cursor.execute('''
            SELECT u.first_name,
            u.last_name,
            u.vk_id,
            u.vk_link,
            du.vk_id
            FROM users AS u
            LEFT JOIN dating_users AS du 
            ON u.vk_id = du.vk_id
            WHERE du.vk_id IS NULL
            OFFSET '{offset}'
            );
        ''')


def drop_users():
    with connection.cursor() as cursor:
        cursor.execute('''
            DROP TABLE IF EXISTS users CASCADE;
            );
        ''')
        print('[INFO] Table users was deleted.')



def drop_dating_users():
    with connection.cursor() as cursor:
        cursor.execute('''
            DROP TABLE  IF EXISTS dating_users CASCADE;
            );
        ''')
        print('[INFO] Table dating_users was deleted.')


def creating_database():
    drop_users()
    drop_dating_users()
    create_users()
    create_dating_users()