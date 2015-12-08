from autobahn.twisted.websocket import WebSocketServerProtocol, \
    WebSocketServerFactory
from motor import Motor
import RPi.GPIO as GPIO
from time import sleep
from twisted.internet.task import LoopingCall, CooperativeTask

class MyServerProtocol(WebSocketServerProtocol):

    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        self.leftmotor = Motor([12, 16, 20, 21])
        self.leftmotor.rpm = 20
        self.rightmotor = Motor([18, 23, 24, 25])
        self.rightmotor.rpm = 20
        self.left_status = 0
        self.right_status = 0
        self.loopingl = None    
        self.loopingr = None    
        self.rate = .02


    def onConnect(self, request):
        print("Client connecting: {0}".format(request.peer))

    def onOpen(self):
        print("WebSocket connection open.")

    def onMessage(self, payload, isBinary):
        if isBinary:
            print("Binary message received: {0} bytes".format(len(payload)))
        else:
            print("Text message received: {0}".format(payload.decode('utf8')))
        if payload == "forward":
            self.loopingl = LoopingCall(self.leftmotor.move_cw, 8)
	    self.loopingl.start(.01, now=True)
	    self.loopingr = LoopingCall(self.rightmotor.move_acw, 8)
	    self.loopingr.start(.01, now=True)
    
        elif payload == "stop":
	    if self.loopingl != None and self.loopingl.running:
		    self.loopingl.stop()
	    if self.loopingr != None and self.loopingr.running:
		self.loopingr.stop()
	elif payload == "left":
	    self.loopingl = LoopingCall(self.leftmotor.move_acw, 8)
	    self.loopingl.start(self.rate, now=True)
	    self.loopingr = LoopingCall(self.rightmotor.move_acw, 8)
	    self.loopingr.start(self.rate, now=True)
        elif payload == "right":
	    self.loopingl = LoopingCall(self.leftmotor.move_cw, 8)
	    self.loopingl.start(self.rate, now=True)
	    self.loopingr = LoopingCall(self.rightmotor.move_cw, 8)
	    self.loopingr.start(self.rate, now=True)
	elif payload == "reverse":
	    self.loopingl = LoopingCall(self.leftmotor.move_acw, 8)
	    self.loopingl.start(self.rate, now=True)
	    self.loopingr = LoopingCall(self.rightmotor.move_cw, 8)
	    self.loopingr.start(self.rate, now=True)
        
        #echo back message verbatim
        self.sendMessage(payload, isBinary)

    def onClose(self, wasClean, code, reason):
        print("WebSocket connection closed: {0}".format(reason))
    GPIO.cleanup()

if __name__ == '__main__':

    import sys
    import socket
    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("gmail.com",80))
    ip = s.getsockname()[0]
    s.close()

    factory = WebSocketServerFactory(u"ws://{0}:9000".format(ip), debug=False)
    factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    reactor.listenTCP(9000, factory)
    reactor.run()
