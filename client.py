from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def status():  # функция для аутентификации
    stat = input('Are you registered user? y/n? Press any key to quit\n')
    global answer
    if stat == "y":
        login = input("Enter login name: ")
        passw = input("Enter password: ")
        answer = stat, login, passw
    elif stat == "n":
        login = input("Create login name: ")
        nick = input("Create nickname: ")
        passw = input("Enter password: ")
        answer = stat, login, nick, passw

    else:
        return quit()
    answer = ','.join(answer)
    return answer

def receive():
    """Обрабатывает прием сообщений."""
    client_socket.send(answer.encode())
    if client_socket.recv(BUFSIZ) == bytes('Authentication Error', 'utf-8'):
        print('Authentication Error')
        client_socket.close()

    while True:
        try:
            print(client_socket.recv(BUFSIZ).decode("utf8"))
        except OSError:  # Возможно, клиент покинул чат.
            quit()

def send():
    """Обрабатываем отправку сообщения"""
    try:
        while True:
            msg = input()
            client_socket.send(bytes(msg, "utf8"))
            if msg == "{quit}":
                client_socket.close()
                quit()
    except:
        client_socket.close()
        quit()

HOST = input('Enter host: ')
PORT = input('Enter port: ')
status()

if not PORT:
    PORT = 9997
else:
    PORT = int(PORT)

BUFSIZ = 1024
ADDR = (HOST, PORT)

client_socket = socket(AF_INET, SOCK_STREAM)
client_socket.connect(ADDR)

receive_thread = Thread(target=receive)
send_thread = Thread(target=send)
send_thread.start()
receive_thread.start()


