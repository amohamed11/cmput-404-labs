import socket
import time
from client import create_tcp_socket, get_remote_ip, send_data


def main():
    try:
        # define address info, payload, and buffer size
        host = ''
        port = 8001
        buffer_size = 4096

        # make the socket, get the ip, and connect
        s = create_tcp_socket()

        remote_ip = get_remote_ip(host)

        s.connect((remote_ip, port))
        print(f'Socket Connected to {host} on ip {remote_ip}')

        # send the data and shutdown
        payload = f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'
        send_data(s, payload)
        s.shutdown(socket.SHUT_WR)

        # continue accepting data until no more left
        full_data = b""
        while True:
            data = s.recv(buffer_size)
            if not data or (len(data) < 5 and data.decode() == 'DONE'):
                break
            full_data += data
        print(full_data)
    except Exception as e:
        print(e)
    finally:
        # always close at the end!
        s.close()


if __name__ == "__main__":
    main()
