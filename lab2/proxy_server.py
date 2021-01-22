#!/usr/bin/env python3
import socket
import time
from client import send_data, get_remote_ip, create_tcp_socket
from multiprocessing import Process, Pool

# define address & buffer size
HOST = ""
PORT = 8001
BUFFER_SIZE = 4096


def sendToGoogle(payload):
    try:
        # define address info, payload, and buffer size
        host = 'www.google.com'
        port = 80

        # make the socket, get the ip, and connect
        s = create_tcp_socket()

        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        remote_ip = get_remote_ip(host)

        s.connect((remote_ip, port))

        send_data(s, payload)
        s.shutdown(socket.SHUT_WR)

        # continue accepting data until no more left
        full_data = b""
        while True:
            data = s.recv(BUFFER_SIZE)
            if not data:
                break
            full_data += data
        return full_data
    except Exception as e:
        print(e)
    finally:
        # always close at the end!
        s.close()


def startServer():
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
            payload = conn.recv(BUFFER_SIZE)
            if len(payload) > 0:
                response = b""
                with Pool(4) as p:
                    reponse = p.apply(sendToGoogle, args=(str(payload),))
                conn.sendall(response)
            time.sleep(0.5)
            conn.close()


if __name__ == "__main__":
    startServer()
    # processes = [Process(target=startServer, args=(googleSocket, ))
    #         for x in range(4)]

    # # Run processes
    # for p in processes:
    #     p.start()

    # # Exit the completed processes
    # for p in processes:
    #     p.join()
