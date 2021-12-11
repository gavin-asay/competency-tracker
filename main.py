from login import login
import sqlite3

connection = sqlite3.connect('competencytracker.db')
cursor = connection.cursor()

login(cursor, connection)
