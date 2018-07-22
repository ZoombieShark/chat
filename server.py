import socket
import sqlrequests
import threading

HOST = ""  # адрес сервера
PORT = 9999  # номер порта от 1024 до 65525
BUFSIZ = 1024  # размер буфера 1 Кбайт
ADDR = (HOST, PORT)  # адрес сервера

tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создает TCP/IP сокет сервера
tcpSerSock.bind(ADDR)  # связываем сокет с адресом

tcpSerSock.listen()  # слушаем клиентов

while True:  # бесконечный цикл сервера
    print('Waiting for client...')
    tcpCliSock, addr = tcpSerSock.accept()  # Ждем клиента,при присоединении .accept() вернет имя сокета
                                            # клиента и его адрес (создаст временный сокет tcpCliSock)
    print('Connected from: {}'.format(addr))
    while True:  # цикл связи
        data = tcpCliSock.recv(BUFSIZ)  # принимает данный от клиента
        if not data:
            break
        answer = (data.decode('utf8')).split(',')  # декодируем сообщение от клиента о авторизации
        print(answer)
        if answer[0] == 'n':  # начало блока аутентофикации
            if sqlrequests.add_user(answer[1], answer[2], answer[3]) == False:
                tcpCliSock.send(bytes('Authentication Error'), 'utf8')
            else:
                tcpCliSock.send(bytes('User Successfully Created'), 'utf8')
        elif answer[0] == 'y':
                if sqlrequests.authenticated(answer[1], answer[2]) == True:
                    tcpCliSock.send(bytes('Access is allowed', 'utf-8'))
                else:
                    tcpCliSock.send(bytes('Authentication Error', 'utf-8'))
    tcpCliSock.close()  # закрываем сеанс с клиентом

def handle_client(client, nick):  # берём сокет клиента и никнейм как агрумент?
    """Обрабатываем соединение одного клиента."""
    name = client.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! If you ever want to quit, type {quit} to exit.' % name
    client.send(bytes(welcome, "utf8"))
    msg = "%s has joined the chat!" % name
    broadcast(bytes(msg, "utf8"))
    while True:
        msg = client.recv(BUFSIZ)
        if msg != bytes("{quit}", "utf8"):
            broadcast(msg, name + ": ")
        else:
            client.send(bytes("{quit}", "utf8"))
            client.close()
            del clients[client]
            broadcast(bytes("%s has left the chat." % name, "utf8"))
            break

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""

    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)


tcpSerSock.close()  # закрытие сокета сервера



