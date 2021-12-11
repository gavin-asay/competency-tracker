import sqlite3
from bcrypt import hashpw, gensalt


def db_setup(cursor):
    with open('db_schemas/schema.sql', 'rt') as schema:
        command = ''
        for line in schema.readlines():
            command += line
            if ';' in line:
                cursor.execute(command)
                command = ''
    connection.commit()

    with open('db_schemas/add_test_data.sql', 'rt') as testdata:
        command = ''
        for line in testdata.readlines():
            command += line
            if ';' in line:
                print(command)
                cursor.execute(command)
                command = ''
    connection.commit()

    passwords = cursor.execute('SELECT password FROM Users').fetchall()

    for i, pw in enumerate(passwords):
        encoded = pw[0].encode('utf-8')
        cursor.execute('UPDATE USERS SET password = ? WHERE user_id = ?',
                       (hashpw(encoded, gensalt()), i + 1))
        connection.commit()


connection = sqlite3.connect('competencytracker.db')
cursor = connection.cursor()

result = db_setup(cursor)
