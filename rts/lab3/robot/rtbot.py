from pyrobot import *
import sys
import logging
import time
import SocketServer
import Queue
import threading

BUFFER_SIZE = 1024
COMMANDS = []
ACK = "ACK\n"
CONFIG_CMD = "__cfg_"
q = Queue.Queue()
p = Queue.Queue()

class RobotController(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.rtbot = robot
    def run(self):
        currentCommand = ''
        while currentCommand != "quit":
            currentCommand = q.get()
            if currentCommand == "forward":
                self.rtbot.DriveStraight(200)
            elif currentCommand == "reverse":
                self.rtbot.DriveStraight(-200)
            elif currentCommand == "left":
                self.rtbot.TurnInPlace(200, "ccw")
            elif currentCommand == "right":
                self.rtbot.TurnInPlace(200, "cw")
            elif currentCommand == "stop":
                self.rtbot.Stop()
        self.rtbot.Stop()


class TCPHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024).strip()
        q.put(self.data)
        if self.data == "quit":
            p.put(self.data)


class safetyController(threading.Thread):
    def __init__(self, robot):
        threading.Thread.__init__(self)
        self.rtbot = robot
    def run(self):
        while True:
            if not p.empty():
                break
            try:
                self.rtbot.sensors.GetAll()
            except PyRobotError:
                pass
            bump = self.rtbot.sensors.GetBump()
            cliff = self.rtbot.sensors.data['cliff-front-right'] or \
                    self.rtbot.sensors.data['cliff-front-left'] or \
                    self.rtbot.sensors.data['cliff-right'] or \
                    self.rtbot.sensors.data['cliff-left']
            wheelDrop = self.rtbot.sensors.data['wheel-drop-left'] or \
                         self.rtbot.sensors.data['wheel-drop-right']
            analogInput = self.rtbot.sensors.GetAnalogInput()

            if wheelDrop:
                q.put("quit")
                break

            if bump: 
                self.rtbot.DriveDistance(-200, 100) 

            if cliff:
                self.rtbot.DriveDistance(-200, 100)

            if analogInput < 30:
                self.rtbot.DriveDistance(-200, 100)
        
#=============================================================
# define the Rtbot class to init and start itself
class Rtbot(Create):
    def __init__(self, tty='/dev/ttyUSB0'):
        super(Create, self).__init__(tty)
        self.sci.AddOpcodes(CREATE_OPCODES)
        self.sensors = CreateSensors(self)
        self.safe = False  # Use full mode for control.

    def start(self):
        logging.debug('Starting up the Rtbot.')
        self.SoftReset()
        self.Control()

    def DriveDistance(self, velocity, distance):
        self.sensors.GetDistance()
        self.DriveStraight(velocity)
        dist = 0
        while(abs(dist) < distance):
            dist += self.sensors.GetDistance()
        self.Stop()

    def TurnAngle(self, velocity, degree, direction):
        self.sensors.GetAngle()
        self.TurnInPlace(velocity, direction)
        angle = 0
        while(abs(angle) < degree):
            angle += self.sensors.GetAngle()
        self.Stop()

#=============================================================
#place further functions in the Rtbot class e.x.
# def somefunction(some_argvs):
#   some code


# To implement a service, you must derive a class from BaseRequestHandler and redefine its handle() method


#subclass of threading.Thread
#override the run() method in a subclass	
    			
    		
