import sys
from socket import *

#Utils

class Server:
    IP_RUN = "10.0.0.4"
    #IP_RUN = "localhost"
    IP = "13.68.241.101"
    #IP = "localhost"
    PORT = 9000
    ADDRESS = (IP, PORT)

class Codes:
    CONN_REQ = "$$conn_req$$"
    CONN_ACK = "$$conn_ack$$"
    PACK_ACK = "$$pack_ack$$"
    KEEP_ALIVE = "$$keep_alive$$"

def createServerSocket():
    socketserv = socket(AF_INET, SOCK_DGRAM)
    socketserv.bind((Server.IP_RUN, Server.PORT))
    return socketserv

def createClientSocket(timeout):
    sock = socket(AF_INET, SOCK_DGRAM)
    sock.settimeout(1)
    return sock

def getPeer(sock, pin):
    print "Waiting for peer to connect..."
    sock.sendto(pin, Server.ADDRESS)
    for i in range(0, 60):
        try:
            data, source = sock.recvfrom(4096)
            if data != Codes.CONN_ACK:
                print "Peer address: %s", data
                splitSTR = data.split(':')
                ip = splitSTR[0]
                port = int(splitSTR[1])
                return ip, port
                break
        except:
            if i % 10 == 0:
                print "%d seconds left for peer to connect..." % (60-i)
            if i == 59:
                print "Failed to connect to peer!"
                print "Exiting program..."
                sys.exit()

def connectToServer(sock):
    print "Attempting to connect to server..."
    for i in range(0, 3):
        try:
            sent = sock.sendto(Codes.CONN_REQ, Server.ADDRESS)
            data, source = sock.recvfrom(4096)
            if data == Codes.CONN_ACK:
                print "Successfully connected to server!"
                break
        except timeout:
            print "Attempt %d..." % (i+1)
            if i == 2:
                print "Failed to connect to server!"
                print "Exiting program..."
                sys.exit()

def connectToPeer(sock, peer):
    print "Attempting to connect to peer..."
    for i in range(0, 10):
        try:
            sent = sock.sendto(Codes.CONN_REQ, peer)
            data, source = sock.recvfrom(4096)
            sock.sendto(Codes.CONN_ACK, peer)
            if data == Codes.CONN_ACK:
                print "Successfully connected to peer!"
                break
        except timeout:
            print "Attempt %d..." % (i+1)
            if i == 9:
                print "Failed to connect to peer!"
                print "Exiting program..."
                sys.exit()