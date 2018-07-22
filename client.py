import socket

def status():
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
        quit()
    answer = ','.join(answer)
    return answer

status()

HOST = 'localhost'
PORT = 9999
BUFSIZ = 1024
ADDR = (HOST, PORT)

tcpCliSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpCliSock.connect(ADDR)

tcpCliSock.send(answer.encode())  # отправка данных в bytes
data = tcpCliSock.recv(BUFSIZ)
print(data.decode('utf8'))
tcpCliSock.close()