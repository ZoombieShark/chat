import sqlite3

conn = sqlite3.connect('chat.db')
cursor = conn.cursor()

try:
    cursor.execute('''CREATE TABLE users 
                      (id INTEGER, user_name VARCHAR, 
                      login VARCHAR, password VARCHAR, date_of_registration DATE,
                      primary key (id)
                      )
                   ''')
    cursor.execute('''CREATE TABLE chat
                      (id INTEGER, message VARCHAR,
                      date_of_message DATE, user_name VARCHAR,
                      primary key (id)
                      )
                   ''')
except:
    pass


