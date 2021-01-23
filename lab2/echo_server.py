#!/usr/bin/env python3
import socket
import time
from multiprocessing import Pool

# define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 1024


def handleConnection(conn):
    full_data = conn.recv(BUFFER_SIZE)
    time.sleep(0.5)
    conn.sendall(full_data)
    conn.sendall("DONE".encode())
    conn.close()


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

        # QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # bind socket to address
        s.bind((HOST, PORT))
        # set to listening mode
        s.listen(2)

        # continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)

            # recieve data, wait a bit, then send it back
            p = Pool(1)
            p.apply(handleConnection, args=(conn,))


if __name__ == "__main__":
    main()
