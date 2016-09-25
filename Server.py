import sys
import time
import socket
import thread
from socket import *

# A simple TCP listener using python sockets

HOST_IP = 'localhost' # listen on local host
HOST_PORT = 8090  # listen on port 8099
DATA_BUFFER = 4096  # allocation for data buffer coming from socket connection


def socketDataRead(remotesocket, addr):
    while 1:
        content = remotesocket.recv(DATA_BUFFER)
        'SocketAdapter --> Handler received data!'
        if not content:
            print 'SocketAdapter --> INVALID DATA'
            break
        print 'SocketAdapter --> Data received from remote host content: ' + content
    remotesocket.close()

def socketDataWrite(remotesocket, addr):
    print 'Writing'
    while 1:
        content = raw_input('Enter your input:')
        remotesocket.send(content)
        'SocketAdapter --> Handler sent data!'
        print 'SocketAdapter --> Data sent: ' + content
    remotesocket.close()

def setup():
    print 'SocketAdapter --> Setting up socket connection...'
    LOCATION = (HOST_IP, HOST_PORT)
    print 'SocketAdapter --> Initializing new socket object...'
    socketserv = socket(AF_INET, SOCK_STREAM)
    socketserv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print 'SocketAdapter --> Binding local host on port ' + str(HOST_PORT)
    socketserv.bind(LOCATION)
    socketserv.listen(5)
    print 'SocketAdapter --> Setting up socket connection...DONE.'
    print 'SocketAdapter --> Listening on port ' + str(HOST_PORT)
    return socketserv


# Main socket server initiator
def runSocketServer():
    socketserver = setup()
    while 1:
        remote_socket = None
        remote_address = None
        # accepting connection from remote machine
        try:
            remote_socket, remote_address = socketserver.accept()
        except:
            print 'SocketAdapter --> Keyboard Interrupt!'
            sys.exit()

        print 'SocketAdapter --> Connection received from: %s' % (remote_address[0])
        thread.start_new_thread(socketDataRead, (remote_socket, remote_address))
        thread.start_new_thread(socketDataWrite, (remote_socket, remote_address))
