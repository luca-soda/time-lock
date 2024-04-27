import psycopg2
from os import getenv

CONNECTION_STRING = getenv('CONNECTION_STRING')
if (CONNECTION_STRING is None):
    raise Exception('CONNECTION_STRING is not defined in .env file')

def init_db():
    connection = psycopg2.connect(CONNECTION_STRING)
    connection.autocommit = True
    cursor = connection.cursor()
    try:
        cursor.execute('CREATE DATABASE time_lock')
    except psycopg2.errors.DuplicateDatabase:
        pass
    connection.close()
    connection = psycopg2.connect(CONNECTION_STRING, database='time_lock')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS key_entry (
        release_date INT,
        uuid TEXT,
        secret TEXT,
        prime TEXT
    )''')
    connection.commit()
    connection.close()

def add_key_entry(release_date: int, uuid: str, secret: str, prime: int):
    connection = psycopg2.connect(CONNECTION_STRING, database='time_lock')
    cursor = connection.cursor()
    cursor.execute('INSERT INTO %s (release_date, uuid, secret, prime) VALUES (%%s, %%s, %%s, %%s)' % 'key_entry', [release_date, uuid, secret, prime])
    connection.commit()
    connection.close()

def find_key_entry(uuid: str):
    connection = psycopg2.connect(CONNECTION_STRING, database='time_lock')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM %s WHERE uuid = %%s' % 'key_entry', [uuid])
    result = cursor.fetchone()
    connection.close()
    if (result is None):
        return None
    return {
        'release_date': result[0],
        'uuid': result[1],
        'secret': result[2],
        'prime': result[3]
    }