import socket
from threading import Thread
import threading
import time

def closeClientSock(clientSock):
    clientSock.shutdown(socket.SHUT_RDWR)
    clientSock.close()
        
# -------------------------------------------------- #
def thread_client(clientSock):
    # Authenticating User
    try:
        clientSock.send(str.encode('Enter userName : '))
        username=clientSock.recv(2048).decode('utf-8')
        clientSock.send(str.encode('Enter password : '))
        password=clientSock.recv(2048).decode('utf-8')
    except: # if client terminates during auth
        return
    if(password!="SECRET"): # if password is wrong
        clientSock.send(str.encode('Incorrect password !!!\nClosing the connection . . .'))
        time.sleep(1)
        clientSock.send(str.encode('exit'))
        closeClientSock(clientSock)
        return
    else:
        allClients.add(clientSock)
        clientSock.send(str.encode(f"Hey {username} !\n>>>>>>> Welcome to the chat room <<<<<<<\nType 'Exit' to terminate connection."))
        while(True):
            data=(clientSock.recv(2048)).decode('utf-8')
            if(data.lower()=="exit"): # If client terminate during chat
                clientSock.send(str.encode('exit'))
                allClients.remove(clientSock)
                closeClientSock(clientSock)
                return
            else:
                msg=f'{username}: '+data
                # Send msg to all except the sender
                for client in allClients :
                    if (client!=clientSock):
                        client.sendall(str.encode(msg))

# create a connection oriented IPv4 socket object
serverSocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Server IP and Port address
host='127.0.0.1'
port=20555

# bind the port and ip to socket
try:
    serverSocket.bind((host,port))
    # queue up to 5 request
    serverSocket.listen(5)
    print(f'Listening at {host}:{port} . . .')

except socket.error as e:
    print(str(e))

# establish a connection to a client
allClients=set()
while(True):
    clientSocket,addr=serverSocket.accept()
    print(f'Connected to {addr[0]}:{addr[1]}')
    t=Thread(None,target=thread_client,args=(clientSocket,))
    t.start()
