from socket import socket
import socket
from socket import *
import sys
import thread

#Client

DATA_BUFFER = 4096
SUCCESS = 201
SUCCESS_WITH_CLIENT = 202

def socketDataRead(relay_socket):
    while 1:
        content = relay_socket.recv(DATA_BUFFER)
        if not content:
            print 'SocketAdapter --> INVALID DATA'
            break
        print 'Recepient:      ' + str(content)
    relay_socket.close()

def socketDataWrite(relay_socket):
    while 1:
        content = None
        content = raw_input('Enter Message: ')
        if content:
            print 'Me:      ' + str(content)
            relay_socket.send(content)
    relay_socket.close()

def manageChat(relay_socket):
    print 'Client --> Handling Chat!'
    print 'Client --> Handling Read Thread!'
    thread.start_new_thread(socketDataRead,(relay_socket,))
    print 'Client --> Handling Write Function!'
    socketDataWrite,(relay_socket)


def handleResponseAndTalk(relay_socket):
    client_response = relay_socket.recv(DATA_BUFFER)

    if str(client_response) == str(SUCCESS_WITH_CLIENT):
        print 'Client --> Successful connection has established!!!'
        manageChat(relay_socket)
    else:
        print 'Client --> Bad response from server!'


def promptUserCode(relay_socket):
    PIN = raw_input("Enter authentication PIN (4 numbers) to talk to the other person: ")
    print 'Client --> Sending PIN to Relay....'
    try:
        relay_socket.send(PIN)
        print 'Client --> Sending PIN to Relay....DONE. Waiting for other person to respond..'
    except Exception as e:
        print 'Client --> Failed to send pin to Relay. Connection will be closed.'
        relay_socket.close()
        sys.exit()

    try:
        handleResponseAndTalk(relay_socket)
    except Exception as e:
        print 'Client --> Failed CHAT. Reason: ' + str(e)


def handleConnectionEstablishment(relay_socket):

    success_code = relay_socket.recv(DATA_BUFFER)

    if str(SUCCESS) == str(success_code):
        print 'Client --> Successful connection with Relay! Follow next step.'
        promptUserCode(relay_socket)
    else:
        print 'Client --> Could not receive data on  connection with relay'


def initiateRelayConnection(relay_ip, relay_port):
    print 'Client --> Setting up socket connection with Relay....'
    locationTuple = (relay_ip, relay_port)
    socketWithRelay = socket(AF_INET, SOCK_STREAM)
    #socketWithRelay.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    print 'Client --> Connecting to relay......'
    try:
        socketWithRelay.connect(locationTuple)
        print 'Client --> Connecting to relay......ESTABLISHED'
        handleConnectionEstablishment(socketWithRelay)
    except Exception as e:
        print 'Client --> Failed connecting the socket with ' + relay_ip + ' on port ' + relay_port
        print 'Exception: ' + str(e)
        print 'Client --> Exiting...'
        socketWithRelay.close()
        sys.exit()


def runClient():

    relayAddr = raw_input("Enter Relay's IP address with port (xxx.xxx.xxx.xxx:port):")
    splitSTR = relayAddr.split(':')

    relayIPAddress = splitSTR[0]
    relayPort = int(splitSTR[1])

    initiateRelayConnection(relayIPAddress, relayPort)