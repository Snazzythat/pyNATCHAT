from Utils import *
from socket import *
import sys
import threading
from datetime import datetime
import time
import os

#Client

SEND_TIME = 2
CHECK_TIME = 6
LAST_CHECK = datetime.now()

def clientRead(sock):
    while 1:
        try:
            data, source = sock.recvfrom(4096)
            if data != Codes.CONN_ACK and data != Codes.CONN_REQ and data != Codes.KEEP_ALIVE:
                print "Peer: %s" % data
            global LAST_CHECK
            LAST_CHECK = datetime.now()
        except timeout:
            pass

def clientWrite(sock, peer):
    while 1:
        try:
            message = raw_input("")
            sock.sendto(message, peer)
        except Exception as e:
            print e

def keepAlive(sock, peer):
    while 1:
        try:
            time.sleep(SEND_TIME)
            sock.sendto(Codes.KEEP_ALIVE, peer)
        except Exception as e:
            print e

def checkConnStatus():
    while 1:
        time.sleep(1)
        diff = datetime.now() - LAST_CHECK
        if diff.seconds > CHECK_TIME:
            print "Disconnected from peer!"
            print "Exiting program..."
            os._exit(0)

def runClient():
    try:
        sock = createClientSocket(1)
        connectToServer(sock)
        pin = raw_input("Enter authentication PIN (4 numbers) to talk to the other person: ")
        peer = getPeer(sock, pin)
        print "Connected to Peer: %s" % str(peer)
        connectToPeer(sock, peer)
        write = threading.Thread(target=clientWrite, args=(sock, peer))
        write.start()
        read = threading.Thread(target=clientRead, args=(sock,))
        read.start()
        sendStatus = threading.Thread(target=keepAlive, args=(sock, peer))
        sendStatus.start()
        checkStatus = threading.Thread(target=checkConnStatus, args=())
        checkStatus.start()
    except:
        sys.exit()