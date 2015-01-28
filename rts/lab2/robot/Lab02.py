import sys
from sys import stdin
from rtbot import *
import logging
import time
import SocketServer
import socket
import threading
import Queue
import signal

HOST = ''
PORT = 50000

FORMAT = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%H%M%S'

def main():
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATE_FORMAT)

    commandQueue = Queue.Queue()

    # Setup and start TCP server
    server = SocketServer.TCPServer((HOST, PORT), TCPHandler)
    server.allow_reuse_address = True
    serverThread = threading.Thread(target=server.serve_forever)
    serverThread.daemon = True
    serverThread.start()

    # Setup and start controller thread
    global robot
    robot = Rtbot(sys.argv[1])
    controllerThread = RobotController(robot)
    controllerThread.start() 

    # Block until controller closes
    controllerThread.join()
    server.shutdown()

        
if __name__ == '__main__':
  main()
