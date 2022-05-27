from recognition import rec
import socket
import pickle
import cv2


def connUser(conn, addr):
    while True:
        mess = conn.recv(1024)
        message = mess.decode()
        
        if message == "download image":
            conn.send(b"done")
            leng = conn.recv(1024)
            length = leng.decode()
            conn.send(length.encode())
            image = bytearray() # Массив для сохранения изображения
            s = 0
            while True:
                m = conn.recv(1024)
                image += m 
                s += len(m)
                if not m or s == int(length):
                    break
            data = rec(pickle.loads(image))
            byteDate = pickle.dumps(data)
            conn.send(byteDate)


        if not mess:
            print("close", addr)
            conn.close() # Выключене сокета
            break
