import sys
import time
import socket
import thread
from socket import *

# A simple TCP listener using python sockets

HOST_IP = '192.168.1.129'  # listen on local host
HOST_PORT = 9091  # listen on port 8099
DATA_BUFFER = 4096  # allocation for data buffer coming from socket connection
MAPPING = {}  # Create empty client dictionary


def connectClients(client1, client2):
    client1.send('202')
    client2.send('202')
    thread.start_new_thread(clientReadWrite, (client1, client2))
    thread.start_new_thread(clientReadWrite, (client2, client1))


def clientReadWrite(read, write):
    try:
        while 1:
            content = read.recv(DATA_BUFFER)
            print 'SocketAdapter --> Handler received data!'
            print str(content)
            print 'SocketAdapter --> Data received from remote host content: ' + content
            write.send(content)
            print 'SocketAdapter --> Data forwarded'
    except Exception as e:
        print str(e)
        read.close()
        write.close()


def setup():
    print 'SocketAdapter --> Setting up socket connection...'
    LOCATION = (HOST_IP, HOST_PORT)
    print 'SocketAdapter --> Initializing new socket object...'
    socketserv = socket(AF_INET, SOCK_STREAM)
    socketserv.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print 'SocketAdapter --> Binding local host on port ' + str(HOST_PORT)
    socketserv.bind(LOCATION)
    socketserv.listen(20)
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
        print 'SocketAdapter --> Staring new thread with %s' % (remote_address[0])
        thread.start_new_thread(readPin, (remote_socket,))
        print 'SocketAdapter --> Listening for more connections...'


def readPin(socket):
    socket.send('201')
    pin = socket.recv(DATA_BUFFER)
    pin = pin.replace('\n', '')
    pin = pin.replace('\t', '')
    pin = pin.replace('\r', '')
    print 'SocketAdapter --> Pin entered: %s' % str(pin)
    print str(MAPPING)
    print '--%s--' % pin
    if pin in MAPPING.keys():
        print 'SocketAdapter --> Pin -%s- FOUND!' % str(pin)
        print 'SocketAdapter --> Establishing connection'
        thread.start_new_thread(connectClients, (MAPPING[pin], socket))
        del MAPPING[pin]
    else:
        print 'SocketAdapter --> Pin -%s- not found, added to mapping' % pin
        MAPPING[pin] = socket
        print str(MAPPING)
