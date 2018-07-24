import socket
import sqlrequests
import threading
import time

HOST = ""  # адрес сервера
PORT = 9999  # номер порта от 1024 до 65525
BUFSIZ = 1024  # размер буфера 1 Кбайт
ADDR = (HOST, PORT)  # адрес сервера
clients = {}  # словарь пользователей онлайн
addresses = {}  # словарь адрессов

tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # создает TCP/IP сокет сервера
tcpSerSock.bind(ADDR)  # связываем сокет с адресом

def accept_incoming_connections():
    while True:
        '''Устанавливаем обработку клиентов'''
        tcpCliSock, addr = tcpSerSock.accept()  # Ждем клиента,при присоединении .accept() вернет имя сокета
                                                # клиента и его адрес (создаст временный сокет tcpCliSock)
        print('Connected from: {}'.format(addr))

        data = tcpCliSock.recv(BUFSIZ)  # принимает данный от клиента
        if not data:
            break
        answer = (data.decode('utf8')).split(',')  # декодируем сообщение от клиента о авторизации

        if answer[0] == 'n':  # начало блока аутентофикации
            if sqlrequests.add_user(answer[1], answer[2], answer[3]) == False:
                tcpCliSock.send(bytes('Authentication Error', 'utf-8'))
                tcpCliSock.close()
            else:
                tcpCliSock.send(bytes('User Successfully Created', 'utf-8'))
                addresses[tcpCliSock] = addr
                threading.Thread(target=handle_client, args=(tcpCliSock, answer[2])).start()
        elif answer[0] == 'y':
            if sqlrequests.authenticated(answer[1], answer[2]) == True:
                tcpCliSock.send(bytes('Access is allowed', 'utf-8'))
                addresses[tcpCliSock] = addr
                nick = sqlrequests.find_nickname(answer[1])
                threading.Thread(target=handle_client, args=(tcpCliSock, nick)).start()
            else:
                tcpCliSock.send(bytes('Authentication Error', 'utf-8'))
                tcpCliSock.close()



def handle_client(client, nick):  # берём сокет клиента и никнейм как агрумент
    """Обрабатывает одно клиентское соединение."""
    welcome = 'Welcome %s!\nView history {msg}\nTo exit {quit}.' % nick
    client.send(bytes(welcome, "utf8"))  # приветствуем клиента
    msg = "%s has joined the chat!" % nick
    broadcast(bytes(msg, "utf8"))  # отправляем функции broadcast сообщение о новом пользователе
    clients[client] = nick

    while True:
        try:
            msg = client.recv(BUFSIZ)
            itstime = time.strftime("%Y-%m-%d-%H.%M.%S", time.localtime())  # время
            sqlrequests.add_messege(msg, itstime, sqlrequests.find_login(nick))  # добавляем в SQLite новое сообщение
            if msg == bytes("{msg}", "utf8"):
                client.send(bytes((sqlrequests.message_history()), 'utf8'))  # отправляем историю сообщений клиенту
            elif msg != bytes("{quit}", "utf8"):
                broadcast(msg, nick + ": ")
            else:
                client.close()
                del clients[client]
                broadcast(bytes("%s has left the chat." % nick, "utf8"))
                break
        except:
            client.close()
            pass

def broadcast(msg, prefix=""):  # префикс для индификации имени
    """Отправлят всем клиентам сообщение от клиента"""
    for sock in clients:
        try:
            sock.send(bytes(prefix, "utf8") + msg)
        except:
            pass




if __name__ == "__main__":
    tcpSerSock.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = threading.Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    tcpSerSock.close()







