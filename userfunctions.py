from utils import getlongest
from bcrypt import hashpw
from getpass import getpass
from re import fullmatch


def getscores(user_id, cursor):
    user_competency_scores = cursor.execute('''SELECT c.name, COALESCE(MAX(r.score), 0)
    FROM Users u
    LEFT JOIN Results r ON r.user_id = u.user_id
    LEFT JOIN Assessments a ON r.assessment_id = a.assessment_id
    LEFT JOIN Competencies c ON a.competency_id = c.competency_id
    WHERE u.user_id = ?
    GROUP BY c.competency_id
    ORDER BY c.competency_id''', (user_id,)).fetchall()

    column_widths = getlongest(user_competency_scores)

    print('0: No competency | 1: Basic competency | 2: Intermediate Competency | 3: Advanced Competency | 4: Expert Competency')
    print(f'{"Competency":<{column_widths[0]}}{"Score":<8}')
    for row in user_competency_scores:
        competency, score = row
        print(f'{competency:<{column_widths[0]}}{score:<8}')


def getassessmenthistory(user_id, cursor):
    user_assessments = cursor.execute('''SELECT a.name, r.score
    FROM Results r
    LEFT JOIN Assessments a ON r.assessment_id = a.assessment_id
    WHERE r.user_id = ?''', (user_id,))

    column_widths = getlongest(user_assessments)

    print('0: No competency | 1: Basic competency | 2: Intermediate Competency | 3: Advanced Competency | 4: Expert Competency')
    print(f'{"Assessment":<{column_widths[0]}}{"Score":<8}')
    for row in user_assessments:
        assessment, score = row
        print(f'{assessment:<{column_widths[0]}}{score:<8}')


def setname(user_id, cursor):
    user = cursor.execute(
        'SELECT firstname, lastname FROM Users WHERE user_id = ?', (user_id,)).fetchone()
    print(f"""First Name: {user[0]}
Last Name: {user[1]}
""")

    new_firstname = input(
        'Enter new first name (blank for no change): ') or user[0]
    new_lastname = input(
        'Enter new first name (blank for no change): ') or user[1]

    cursor.execute('UPDATE Users SET firstname = ?, lastname = ? WHERE user_id = ?',
                   (new_firstname, new_lastname, user_id))
    print(f'Name set to: {new_firstname} {new_lastname}')


def setemail(user_id, cursor):
    user = cursor.execute(
        'SELECT email FROM Users WHERE user_id = ?', (user_id,)).fetchone()
    print(f'Email Address: {user[0]}')

    new_email = ''
    while not fullmatch(r'[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,4}', new_email):
        new_email = input(
            'Enter new email address (blank for no change/cancel): ') or user[0]

    cursor.execute('UPDATE Users SET email = ? WHERE user_id = ?',
                   (new_email, user_id))
    print(f'Email address set to: {new_email}')


def setpassword(user_id, cursor):
    new_pass = getpass('''Password must contain:
    - Lowercase letter
    - Uppercase letter
    - One or more digits
    
Enter new password: ''')

    cursor.execute('UPDATE Users SET password = ? WHERE user_id = ?',
                   (new_pass, user_id))
    print('Password updated.')


def setphone(user_id, cursor):
    user = cursor.execute(
        'SELECT phone FROM Users WHERE user_id = ?', (user_id,)).fetchone()
    print(f'Phone Number: {user[0]}')

    new_phone = input(
        'Enter new phone number (blank for no change/cancel): ') or user[0]

    cursor.execute('UPDATE Users SET phone = ? WHERE user_id = ?',
                   (new_phone, user_id))
    print(f'Email address set to: {new_phone}')
