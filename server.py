import socket
from threading import Thread


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
hostname = '0.0.0.0'
port = 12344
server.bind((hostname, port))

server.listen(5)

print("Server starts")

clients = []
addresses = []
server.settimeout(0.1)


def conecting():
    try:
        con, addr = server.accept()
        print("Подключился: ", addr)
        con.send("Вы подключились к серверу".encode())
        clients.append(con)
        addresses.append(addr)
    except socket.timeout:
        pass


def answer():
    i = 0
    for con in clients:
        con.settimeout(0.1)
        try:
            data = con.recv(256)
            answ = data.decode()
            if data:
                if answ == "disconnect":
                    clients.remove(con)
                    con.close()
                    print(addresses[i], "  Отключился")
                    addresses.remove(addresses[i])
                    continue
                print(addresses[i], ":  ", data.decode())
        except socket.timeout:
            pass

        i += 1


if __name__ == '__main__':
    while True:
        Tcon = Thread(target=conecting(), daemon=True)
        Tans = Thread(target=answer(), daemon=True)

        Tcon.start()
        Tans.start()

        Tcon.join()
        Tans.join()

