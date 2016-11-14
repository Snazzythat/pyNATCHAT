import sys
import time
import socket
import thread
import Utils
from socket import *

# A simple TCP listener using python sockets

DATA_BUFFER = 4096  # allocation for data buffer coming from socket connection
MAPPING = {}  # Create empty client dictionary

# Main socket server initiator
def runSocketServer():
    socketserver = Utils.createServerSocket()
    while 1:
        # accepting connection from remote machine
        try:
            data, address = socketserver.recvfrom(4096)
            if data == Utils.Codes.CONN_REQ:
                print "Connection request from ", address
                socketserver.sendto(Utils.Codes.CONN_ACK, address)
            else:
                addPin(socketserver, data, address)
        except Exception as e:
            print 'Exception: ' + str(e)
            sys.exit()

def addPin(sock, pin, source):
    pin = pin.replace('\n', '')
    pin = pin.replace('\t', '')
    pin = pin.replace('\r', '')
    print 'SocketAdapter --> Pin entered: %s' % str(pin)
    print str(MAPPING)
    print '--%s--' % pin
    if pin in MAPPING.keys():
        print 'SocketAdapter --> Pin -%s- FOUND!' % str(pin)
        print 'SocketAdapter --> Establishing connection'
        sock.sendto("%s:%d" % (MAPPING[pin][0], MAPPING[pin][1]), source)
        sock.sendto("%s:%d" % (source[0], source[1]), MAPPING[pin])
        del MAPPING[pin]
    else:
        print 'SocketAdapter --> Pin -%s- not found, added to mapping' % pin
        MAPPING[pin] = source
        print str(MAPPING)
