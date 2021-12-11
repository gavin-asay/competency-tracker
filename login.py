from getpass import getpass
from bcrypt import checkpw
from menus import usermenu, managermenu


def login(cursor, connection):
    print('Welcome to Competency Tracker 1.0!')
    email = input('Enter email address: ')
    password = getpass('Enter password: ')

    loginuser = cursor.execute(
        'SELECT email, password, firstname, lastname, is_manager FROM users WHERE email = ?', (email,)).fetchall()

    if not loginuser:
        print('Invalid login credentials.\n')
        return login(cursor, connection)

    encoded = password.encode('utf-8')
    email, pw, firstname, lastname, is_manager = loginuser[0]
    if checkpw(encoded, pw):
        print(f'Welcome, {firstname} {lastname}!')
        if is_manager:
            return managermenu(email, cursor, connection)
            # print('is manager')
        else:
            return usermenu(email, cursor, connection)
            # print('is user')
    else:
        print('Invalid login credentials.\n')
        return login(cursor, connection)
