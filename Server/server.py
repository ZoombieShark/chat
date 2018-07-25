import socket
from Server import sqlrequests
import threading
import time
import json

with open('ServerConfig', 'r') as config:
    pObj = json.load(config)
    HOST = pObj['SERVER'][0]['HOST']
    PORT = pObj['SERVER'][1]['PORT']
    LISTEN = pObj['SERVER'][2]['LISTEN']

#HOST = ""  # адрес сервера
#PORT = 9997  # номер порта от 1024 до 65525
#LISTEN = 5

BUFSIZ = 1024  # размер буфера 1 Кбайт
ADDR = (HOST, int(PORT))  # адрес сервера
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
        try:
            data = tcpCliSock.recv(BUFSIZ)  # принимает данный от клиента
            if not data:
                break
            answer = (data.decode('utf8')).split(',')  # декодируем сообщение от клиента о авторизации
            # print(answer)
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
        except:
            tcpCliSock.close()
            pass

#def close_connection(client, error):
#    client.send(bytes(error, "utf8"))
#    client.close()

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
                client.send(bytes((sqlrequests.message_history()), 'utf8')) # отправляем историю сообщений клиенту
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
    try:
        tcpSerSock.listen(int(LISTEN))
        print("Waiting for connection...")
        ACCEPT_THREAD = threading.Thread(target=accept_incoming_connections)
        ACCEPT_THREAD.start()
        ACCEPT_THREAD.join()
        tcpSerSock.close()
    except KeyboardInterrupt:
        exit(0)






