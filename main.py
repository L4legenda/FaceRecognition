from recognition import rec
import socket
import pickle
import cv2
from threading import Thread
from connectUser import connUser

print("Socket ON")
sock = socket.socket() # Создание сокета

sock.bind(('', 9090)) # Создание хоста

sock.listen(10) # Количество подключений в хосту

while True:

    conn, addr = sock.accept() # Получение conn = Сокет, addr = Адрес клиента

    print("Connect to ", conn)

    print("addr ", addr)
    Thread(target=connUser, args=(conn, addr)).start()



