import socket
import sys

HOST = "172.17.164.134"
PORT = 50000

data = " ".join(sys.argv[1:])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sock.connect((HOST, PORT))
    sock.sendall(data + "\n")
finally:
    sock.close()

exit(0)
