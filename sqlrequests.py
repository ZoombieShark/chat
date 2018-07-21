import sqlite3, time

db = sqlite3.connect('chat.db')
cursor = db.cursor()

def add_user(login, name, passw):
    chek_login = cursor.execute('''SELECT login FROM users WHERE login = ? ''',(login,))
    if chek_login.fetchone()[0] == login:
        return False
    else:
        cursor.execute('''INSERT INTO users(login, user_name, password, date_of_registration)
                              VALUES(?,?,?,?)
                           ''', (login, name, passw, time.ctime())
                       )
        db.commit()

def authenticated(login, passw):
    if cursor.execute('''SELECT password FROM users WHERE login = ?''',
                      (login,)).fetchone() == (passw,):
        return True


def add_messege(messege, date, name):
    cursor.execute('''INSERT INTO chat(message, date_of_message, user_name) 
                          VALUES(?,?,?)
                       ''', (messege, date, name)
                   )
    db.commit()






