import socket
import sys
from threading import Thread

# Terminator #
def terminate(error):
    print(error)
    exit()
# create clientSocket object
clientSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server's IP and Port address
host='127.0.0.1'
port=20555

# Connect to server
try:
    clientSocket.connect((host,port))
except socket.error as e:
    print(str(e))
    exit()

# AUTHENTICATION
try:
    Reply=clientSocket.recv(1024)
    print(Reply.decode('utf-8'))

    username=input('')
    clientSocket.send(str.encode(username))

    Reply=clientSocket.recv(1024)
    print(Reply.decode('utf-8'))
    password=input('')
    clientSocket.send(str.encode(password))
except socket.error as e: # if clients terminates during auth
    clientSocket.close()
    terminate(e)

# Chit-Chat
def recv_message():
    while(True):
        try:
            Reply=clientSocket.recv(1024).decode('utf-8')
            if(Reply):
                if (Reply=='exit'): # if server closes connection
                    clientSocket.close()
                    return
                else:
                    print(Reply)
        except socket.error as e:
            terminate(e)    

t=Thread(None,target=recv_message) # thread that keep listening for messages
t.start()

while(True):    # Waits for user messages
    if(t.is_alive()):
        try:
            message=input('')
            clientSocket.send(str.encode(message))
        except: # if clients terminates during chat
            try:
                clientSocket.send(str.encode("EXIT"))
            except socket.error as e:
                clientSocket.close()
                terminate("! EXITED")

    else:        
        exit()