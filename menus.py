from userfunctions import *
from managerfunctions import *


def usermenu(email, cursor, connection, manager_access=False):
    user = cursor.execute(
        'SELECT firstname, lastname, phone, hiredate, user_id FROM Users WHERE email = ?', (email,)).fetchone()
    firstname, lastname, phone, hiredate, user_id = user

    menu = f'''Competency Tracker
    User: {firstname} {lastname} | Hired on {hiredate}
    {"MANAGER ACCESS" if manager_access else ""}
    USER MENU
    1. View Competency Scores
    2. View Assessment History
    3. Update Name
    4. Update Email Address
    5. Update Password
    6. Update Phone Number
    7. {"Return to Manager Menu" if manager_access else "Exit"}
    '''

    while True:
        print(menu)
        option = 0
        while option not in range(1, 8):
            option = int(input('Enter a number from the menu: '))

        if option == 1:
            getscores(user_id, cursor)
        elif option == 2:
            getassessmenthistory(user_id, cursor)
        elif option == 3:
            setname(user_id, cursor)
        elif option == 4:
            setemail(user_id, cursor)
        elif option == 5:
            setpassword(user_id, cursor)
        elif option == 6:
            setphone(user_id, cursor)
        elif option == 7:
            print('Exiting user menu ...' if manager_access else 'Goodbye!')
            break

        if option in range(3, 7):
            connection.commit()

    if not manager_access:
        login()


def managermenu(email, cursor, connection):
    manager = cursor.execute(
        'SELECT firstname, lastname, phone, hiredate, user_id FROM Users WHERE email = ?', (email,)).fetchone()
    firstname, lastname, phone, hiredate, user_id = manager

    menu = f'''Competency Tracker
    User: {firstname} {lastname} | Hired on {hiredate}
    
    MANAGER MENU
    1. View User List
    2. Search Users by Name
    3. View/Edit Own Personal Info
    4. Add User
    5. Add Competency
    6. Add Assessment
    7. Add Assessment Result for User
    8. Edit Competency
    9. Edit Assessment
    10. Edit Assessment Result
    11. Delete an Assessment Result
    12. Create Report: Competency Scores for Single User
    13. Create Report: Competency Summary
    14. Import Assessment Results from CSV
    15. Exit
    '''

    def generate_user_submenu(foreign_user_id):
        foreign_user = cursor.execute(
            'SELECT email FROM Users WHERE user_id = ?', (foreign_user_id,)).fetchone()
        # Using clearly set scope for the menu-within-a-menu setup for the sake of data integrity

        def run_user_submenu():
            usermenu(foreign_user[0], cursor, connection, True)
        return run_user_submenu

    while True:
        print(menu)
        option = 0
        while option not in range(1, 16):
            option = int(input('Enter a number from the menu: '))

        if option == 1:
            lookupcheck = getusers(cursor)
            if isinstance(lookupcheck, int):
                foreign_submenu = generate_user_submenu(lookupcheck)
                foreign_submenu()
        elif option == 2:
            lookupcheck = searchusers(cursor)
            if isinstance(lookupcheck, int):
                foreign_submenu = generate_user_submenu(lookupcheck)
                foreign_submenu()
        elif option == 3:
            self_submenu = generate_user_submenu(user_id)
            self_submenu()
        elif option == 4:
            adduser(cursor)
        elif option == 5:
            addcompetency(cursor)
        elif option == 6:
            addassessment(cursor)
        elif option == 7:
            addresult(cursor)
        elif option == 8:
            editcompetency(cursor)
        elif option == 9:
            editassessment(cursor)
        elif option == 10:
            editresult(cursor)
        elif option == 11:
            deleteresult(cursor)
        elif option == 12:
            userdetailreport(cursor)
        elif option == 13:
            competencysummary(cursor)
        elif option == 14:
            csvimport(cursor)
        elif option == 15:
            print('Goodbye!')
            break

        if option in range(3, 12) or option == 14:
            connection.commit()
