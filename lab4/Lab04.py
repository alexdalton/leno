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

FORMAT = '%(asctime)s %(levelname)s [%(filename)s:%(lineno)d] %(message)s'
DATE_FORMAT = '%H%M%S'

def main():
    logging.basicConfig(level=logging.INFO, format=FORMAT, datefmt=DATE_FORMAT)

    commandQueue = Queue.Queue()

    global robot
    robot = Rtbot(sys.argv[1])
    robot.start()

    # Setup and start controller thread
    controllerThread = RobotController(robot)
    controllerThread.start() 

    # Start safety core thread
    safetyCore = safetyController(robot)
    safetyCore.start()

    try:
        api = tweetpony.API("sqjwOmPIc6qfOPR2YVIKTXfMz",
                            "2imj49S2Z0ZWdXc5Nm6nAChEjLa42nLncTnIcnJBBwva2ldLNf",
                            "2902918832-x5y3tFlt2zhbf9u2SLW2uJO289TFSUslxdxemx8",
                            "AqA784KdlzCyGSqeUrz7VlV7ZmrDFKU3krA0ATaqPtcl0")
    except tweetpony.APIError as err:
        print(err.code, err.description)

    processor = StreamProcessor(api)
    try:
        api.user_stream(processor = processor)
    except KeyboardInterrupt:
        pass

    # Block until controller closes
    controllerThread.join()
    server.shutdown()

        
if __name__ == '__main__':
  main()
