import socket
import threading

HOST = "127.0.0.1"
PORT =  9090


server = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
server.bind ( (HOST , PORT) )

server.listen()

clients = []

nicknames = []


def broadcast(message):
    for client in clients:
        client.send(message)
  
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{nicknames[clients.index(client)]}")
            broadcast(message)
        except:
            index= clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.pop()
            break
            



def recieve():
    while True:
        clientSocket , address=server.accept()
        print(f"connected to {str(address)}")
        clientSocket.send("NICKNAME".encode('utf-8'))
        nickname = clientSocket.recv(1024)
        
        nicknames.append(nickname)
        clients.append(clientSocket)
        
        print(f"nickname of client is {nickname} ")
        broadcast(f"{nickname} connected to server!!\n".encode('utf-8'))
        
        thread = threading.Thread(target=handle,args=(clientSocket,))
        #comma to treat it as tuple --> client,
        thread.start()       
        
print("server running")
recieve()