import sqlite3, time

db = sqlite3.connect('chat.db', check_same_thread = False)

cursor = db.cursor()

def add_user(login, name, passw):
    chek_login = cursor.execute('''SELECT login FROM users WHERE login = ? ''',(login,))
    if chek_login.fetchone() == (login, ):
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

def find_nickname(login):
    chek_login = cursor.execute('''SELECT user_name FROM users WHERE login = ? ''', (login,))
    return chek_login.fetchall()[0][0]

def find_login(nick):
    chek_nick = cursor.execute('''SELECT login FROM users WHERE user_name = ? ''', (nick,))
    return chek_nick.fetchall()[0][0]

def message_history():
    msg_story = cursor.execute('''SELECT * FROM chat ''')
    tex = ''
    for _ in msg_story.fetchall():
        ms = _[2], _[3], _[1].decode()
        tex += str(ms)
    return tex



