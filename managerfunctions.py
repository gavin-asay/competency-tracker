from os import error
from os.path import exists
from utils import paginate_list, clear_console, paginate_list_forlookup
from bcrypt import hashpw, gensalt
from re import fullmatch
from datetime import date
import csv


def getusers(cursor):
    users = cursor.execute('''SELECT user_id,
        firstname, 
        lastname,
        IFNULL(phone, 'none'),
        email,
        hiredate,
        CASE WHEN is_manager = 1 THEN "yes" ELSE "no" END,
        CASE WHEN active = 1 THEN "yes" ELSE "no" END
        FROM Users;''').fetchall()

    lookupcheck = paginate_list(users, 'Users')
    if isinstance(lookupcheck, int):
        return lookupcheck


def searchusers(cursor):
    searchterm = input(
        'Enter name or part of name to search both first and last names: ')

    users = cursor.execute('''SELECT user_id,
        firstname, 
        lastname,
        IFNULL(phone, 'none'),
        email,
        hiredate,
        CASE WHEN is_manager = 1 THEN "yes" ELSE "no" END,
        CASE WHEN active = 1 THEN "yes" ELSE "no" END
        FROM Users
        WHERE firstname LIKE ? OR lastname LIKE ?;''', (searchterm, searchterm))

    lookupcheck = paginate_list(users, 'Users')
    if isinstance(lookupcheck, int):
        return lookupcheck


def getcompetencies(cursor):
    competencies = cursor.execute('''SELECT
        competency_id, name, date_created,
        CASE WHEN active = 1 THEN "yes" else "no" END
        FROM Competencies;''').fetchall()

    paginate_list(competencies, 'Competencies')


def adduser(cursor):
    firstname = input('Enter first name (required): ')
    while not firstname:
        firstname = input('Enter first name (required): ')
    lastname = input('Enter last name (required): ')
    while not lastname:
        lastname = input('Enter last name (required): ')
    phone = input('Enter phone number: ')
    email = input('Enter email address (required): ')
    while not email or not fullmatch(r'\S+@\S+\.\S+', email):
        email = input('Enter email address (required): ')
    password = input('Enter user password (required, 8 character minimum): ')
    while len(password) < 8:
        password = input(
            'Enter user password (required, 8 character minimum): ')
    password = password.encode('utf-8')
    encrypted = hashpw(password, gensalt())
    hiredate = input(
        'Enter date of hire, YYYY-MM-DD format. Leave blank for today: ')
    while hiredate and not fullmatch(r'\d{4}-\d{2}-\d{2}', hiredate):
        hiredate = input(
            'Enter date of hire, YYYY-MM-DD format. Leave blank for today: ')
    is_manager = input('Is this user a manager? [y/n] ').lower()
    while is_manager and is_manager not in ('y', 'n'):
        is_manager = input('Is this user a manager? [y/n] ').lower()

    try:
        cursor.execute('''INSERT INTO Users
        (firstname, lastname, phone, email, password, hiredate, is_manager)
        VALUES
        (?,?,?,?,?,?,?)''', (firstname, lastname, phone, email or None, encrypted, hiredate or date.today().strftime('%Y-%m-%d'), 1 if is_manager == 'y' else 0))
    except error:
        clear_console()
        print(error)
        adduser(cursor)


def addcompetency(cursor):
    name = input('Enter competency name (required): ')
    while not name:
        name = input('Enter competency name (required): ')

    try:
        cursor.execute('INSERT INTO Competencies (name) VALUES(?)', (name,))
    except error:
        clear_console()
        print(error)
        addcompetency(cursor)


def addassessment(cursor):
    competencies = cursor.execute('''SELECT
        competency_id, name, date_created,
        CASE WHEN active = 1 THEN "yes" else "no" END
        FROM Competencies;''').fetchall()

    competency_id = paginate_list_forlookup(competencies, 'Competencies')
    while not competency_id:
        competency_id = paginate_list_forlookup(competencies, 'Competencies')
    name = input('Enter assessment name (required): ')
    while not name:
        name = input('Enter assessment name (required): ')

    try:
        cursor.execute(
            'INSERT INTO Assessments (competency_id, name) VALUES (?,?)', (competency_id, name))
    except error:
        clear_console()
        print(error)
        addassessment(cursor)


def addresult(cursor):
    users = cursor.execute('''SELECT user_id,
        firstname, 
        lastname,
        IFNULL(phone, 'none'),
        email,
        hiredate,
        CASE WHEN is_manager = 1 THEN "yes" ELSE "no" END,
        CASE WHEN active = 1 THEN "yes" ELSE "no" END
        FROM Users;''').fetchall()

    assessments = cursor.execute('''SELECT assessment_id,
    competency_id,
    name,
    date_created,
    CASE WHEN active = 1 THEN "yes" ELSE "no" END
    FROM Assessments''')

    user_id = paginate_list_forlookup(users, 'Users')
    while not user_id:
        user_id = paginate_list_forlookup(users, 'Users')
    assessment_id = paginate_list_forlookup(assessments, 'Assessments')
    while not assessment_id:
        assessment_id = paginate_list_forlookup(assessments, 'Assessments')
    score = input('Enter score from 0-4 (required): ')
    while score not in ('0', '1', '2', '3', '4'):
        score = input('Enter score from 0-4 (required): ')
    score = int(score)
    date_taken = input(
        'Enter date taken in YYYY-MM-DD format, leave blank for today: ')
    while date_taken and not fullmatch(r'\d{4}-\d{2}-\d{2}', date_taken):
        date_taken = input(
            'Enter date of hire, YYYY-MM-DD format. Leave blank for today: ')

    try:
        cursor.execute('INSERT INTO Results (assessment_id, user_id, score, date_taken) VALUES (?,?,?,?)',
                       (assessment_id, user_id, score, date_taken or date.today().strftime('%Y-%m-%d')))
    except error:
        clear_console()
        print(error)
        addassessment(cursor)


def editcompetency(cursor):
    competencies = cursor.execute('''SELECT
        competency_id, name, date_created,
        CASE WHEN active = 1 THEN "yes" else "no" END
        FROM Competencies;''').fetchall()

    competency_id = paginate_list_forlookup(competencies, 'Competencies')
    while not competency_id:
        competency_id = paginate_list_forlookup(competencies, 'Competencies')

    name = input('Enter new competency name (leave blank for no change): ')

    if name:
        try:
            cursor.execute(
                'UPDATE Competencies SET name = ? WHERE competency_id = ?', (name, competency_id))
        except error:
            clear_console()
            print(error)
            addassessment(cursor)


def editassessment(cursor):
    assessments = cursor.execute('''SELECT assessment_id,
    competency_id,
    name,
    date_created,
    CASE WHEN active = 1 THEN "yes" ELSE "no" END
    FROM Assessments''')

    assessment_id = paginate_list_forlookup(assessments, 'Assessments')
    while not assessment_id:
        assessment_id = paginate_list_forlookup(assessments, 'Assessments')

    changecomp = input('Do you want to change the competency_id? [y/N]')
    competency_id = None
    if changecomp.lower() == 'y':
        competencies = cursor.execute('''SELECT
        competency_id, name, date_created,
        CASE WHEN active = 1 THEN "yes" else "no" END
        FROM Competencies;''').fetchall()

        competency_id = paginate_list_forlookup(competencies, 'Competencies')
        while not competency_id:
            competency_id = paginate_list_forlookup(
                competencies, 'Competencies')

    name = input(
        'Enter new assessment name (leave blank for no change): ')

    if name:
        values = [name]
        if competency_id:
            values.append(competency_id)
        values.append(assessment_id)

        try:
            cursor.execute(
                f'UPDATE Assessments SET name = ?{", competency_id = ?" if len(values) == 2 else ""} WHERE assessment_id = ?', tuple(values))
        except error:
            clear_console()
            print(error)
            addassessment(cursor)


def editresult(cursor):
    results = cursor.execute('''SELECT r.result_id,
    a.name,
    u.lastname || ", " || u.firstname,
    r.score,
    r.date_taken,
    CASE WHEN r.active = 1 THEN "yes" ELSE "no" END
    FROM Results r
    LEFT JOIN Assessments a ON a.assessment_id = r.assessment_id
    LEFT JOIN Users u ON u.user_id = r.user_id
    ORDER BY u.lastname''')

    result_id = paginate_list_forlookup(results, 'Results')
    while not result_id:
        result_id = paginate_list_forlookup(results, 'Results')

    changeassess = input('Do you want to change the assessment? [y/N]: ')
    assessment_id = None
    if changeassess.lower() == 'y':
        assessments = cursor.execute('''SELECT assessment_id,
        competency_id,
        name,
        date_created,
        CASE WHEN active = 1 THEN "yes" ELSE "no" END
        FROM Assessments''')

        assessment_id = paginate_list_forlookup(assessments, 'Assessments')
        while not assessment_id:
            assessment_id = paginate_list_forlookup(assessments, 'Assessments')

    changeuser = input('Do you want to change the user? [y/N]: ')
    user_id = None
    if changeuser.lower() == 'y':
        users = cursor.execute('''SELECT user_id,
        firstname, 
        lastname,
        IFNULL(phone, 'none'),
        email,
        hiredate,
        CASE WHEN is_manager = 1 THEN "yes" ELSE "no" END,
        CASE WHEN active = 1 THEN "yes" ELSE "no" END
        FROM Users;''').fetchall()

        user_id = paginate_list_forlookup(users, 'Users')
        while not user_id:
            user_id = paginate_list_forlookup(users, 'Users')

    score = input('Enter new score (leave blank for no change): ')
    if score:
        score = int(score)

    if assessment_id or changeuser or score:
        values = []
        if assessment_id:
            values.append(assessment_id)
        if user_id:
            values.append(user_id)
        if score:
            values.append(score)
        values.append(result_id)

        try:
            cursor.execute(f'''UPDATE Results
            SET {"assessment_id = ?," if assessment_id else ""}
            {"user_id = ?," if user_id else ""}
            {"score = ?" if score else ""}
            WHERE result_id = ?''', tuple(values))
        except error:
            clear_console()
            print(error)
            addassessment(cursor)


def deleteresult(cursor):
    results = cursor.execute('''SELECT r.result_id,
    a.name,
    CONCAT(u.lastname, ", ", u.firstname),
    r.score,
    r.date_taken,
    CASE WHEN r.active = 1 THEN "yes" ELSE "no" END
    FROM Assessments r
    LEFT JOIN Assessments a ON a.assessment_id = r.assessment_id,
    LEFT JOIN Users u ON u.user_id = r.user_id
    ORDER BY u.lastname''')

    result_id = paginate_list_forlookup(results, 'Results')

    if result_id:
        try:
            cursor.execute(
                'DELETE FROM Results WHERE result_id = ?', (result_id,))
        except error:
            clear_console()
            print(error)
            addassessment(cursor)


def userdetailreport(cursor):
    users = cursor.execute('''SELECT user_id,
        firstname, 
        lastname,
        IFNULL(phone, 'none'),
        email,
        hiredate,
        CASE WHEN is_manager = 1 THEN "yes" ELSE "no" END,
        CASE WHEN active = 1 THEN "yes" ELSE "no" END
        FROM Users;''').fetchall()

    user_id = paginate_list_forlookup(users, 'Users')

    selecteduser = cursor.execute(
        'SELECT firstname || lastname FROM Users WHERE user_id = ?', (user_id,)).fetchone()
    while not user_id:
        user_id = paginate_list_forlookup(users, 'Users')

    user_competency_scores = cursor.execute('''SELECT IFNULL(MAX(r.score), 0), c.name
        FROM Competencies c
        LEFT JOIN Assessments a ON a.competency_id = c.competency_id
        LEFT JOIN Results r ON r.assessment_id = a.assessment_id AND r.user_id = ?
        GROUP BY c.competency_id
        ORDER BY c.competency_id, r.date_taken''', (user_id,)).fetchall()

    with open(f'reports/scoredetail_{selecteduser[0]}.csv', 'at') as detail:
        wrt = csv.writer(detail)

        wrt.writerow(['Score', 'Competency'])
        wrt.writerows(user_competency_scores)


def competencysummary(cursor):
    competencies = cursor.execute('''SELECT
        competency_id, name, date_created,
        CASE WHEN active = 1 THEN "yes" else "no" END
        FROM Competencies;''').fetchall()

    competency_id = paginate_list_forlookup(competencies, 'Competencies')
    while not competency_id:
        competency_id = paginate_list_forlookup(
            competencies, 'Competencies')

    competencyscores = cursor.execute('''SELECT u.lastname || ", " || u.firstname, MAX(r.score)
        FROM Assessments a
        LEFT JOIN Results  r   ON a.assessment_id = r.assessment_id AND a.competency_id = 1
        LEFT JOIN Users u ON r.user_id = u.user_id
        WHERE u.lastname IS NOT NULL
        GROUP BY r.user_id''').fetchall()

    selectedcompetency = cursor.execute(
        'SELECT name FROM Competencies WHERE competency_id = ?', (competency_id,)).fetchone()

    with open(f'reports/scoresummary_{selectedcompetency[0]}.csv', 'wt') as summary:
        wrt = csv.writer(summary)

        wrt.writerow(['Name', 'Score'])
        wrt.writerows(competencyscores)


def csvimport(cursor):
    filepath = input(
        'Enter the file path and name of the CSV file to import (relative to location of the application): ')
    while not exists(filepath):
        print('File not found.')
        filepath = input(
            'Enter the file path and name of the CSV file to import (relative to location of the application): ')

    newresults = []
    errorlines = []
    with open(filepath, 'rt') as importdata:
        reader = csv.reader(importdata)
        i = 1
        for row in reader:
            user_id, assessment_id, score, date_taken = row
            if user_id == 'user_id':
                continue

            if user_id.isnumeric() and assessment_id.isnumeric() and int(score) in range(5) and fullmatch(r'\d{4}-\d{2}-\d{2}', date_taken):
                newresults.append((user_id, assessment_id, score, date_taken))
            else:
                errorlines.append(str(i))
            i += 1
        if len(newresults) == 1:
            cursor.execute(
                'INSERT INTO RESULTS (user_id, assessment_id, score, date_taken) VALUES (?,?,?,?)', newresults[0])
        elif len(newresults) > 1:
            for row in newresults:
                cursor.execute(
                    'INSERT INTO RESULTS (user_id, assessment_id, score, date_taken) VALUES (?,?,?,?)', row)
        elif len(newresults) == 0:
            print('No readable data in provided file.')

        if len(errorlines):
            print('Invalid data on lines: ' +
                  ', '.join(errorlines) + ' of ' + filepath)
