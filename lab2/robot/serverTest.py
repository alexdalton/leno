import SocketServer
import threading

HOST = ''
PORT = 50000

class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        print self.data

server = SocketServer.TCPServer((HOST, PORT), TCPHandler)
server.allow_reuse_address = True
serverThread = threading.Thread(target=server.serve_forever)
serverThread.daemon = True
serverThread.start()

serverThread.join()
