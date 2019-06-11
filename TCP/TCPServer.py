# Python program to implement server side of chat room. 
import socket 
import select 
from thread import *
import sys
  
"""The first argument AF_INET is the address domain of the 
socket. This is used when we have an Internet Domain with 
any two hosts The second argument is the type of socket. 
SOCK_STREAM means that data or characters are read in 
a continuous flow."""
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
  
# if number of arguments is correct 
if len(sys.argv) != 3: 
    print ("Correct usage: script, IP address, port number")
    exit() 
  
# assigns IP address to first argument
IP_address = str(sys.argv[1]) 
  
# assignts Port to second argument 
Port = int(sys.argv[2]) 
  
""" 
server.bind((IP_address, Port) binds the server to a given IP address
and specified port number.

"""
server.bind((IP_address, Port)) 
  
""" 
server.listen(100) listens for 100 active connections.
"""
server.listen(100) 
  
list_of_clients = [] 
  
def clientthread(conn, addr): 
  
    # sends Welcome message 
    conn.send("Welcome to this chatroom!") 
  
    while True: 
            try: 
                message = conn.recv(2048) 
                if message: 
  
                    """prints the message and address of the 
                    user who just sent the message"""

                    print ("< " + addr[0] + "> " + message)
  
                    # send message to all 
                    message_to_send = "<" + addr[0] + "> " + message 
                    broadcast(message_to_send, conn) 
  
                else: 
                    """if connection is broken"""
                    remove(conn) 
  
            except: 
                continue
  
"""broadcast the message to all 
clients who's object is not the same as the one sending 
the message """
def broadcast(message, connection): 
    for clients in list_of_clients: 
        if clients!=connection: 
            try: 
                clients.send(message) 
            except: 
                clients.close() 
  
                # if the link is broken, we remove the client 
                remove(clients) 
  
"""removes connection"""
def remove(connection): 
    if connection in list_of_clients: 
        list_of_clients.remove(connection) 
  
while True: 
  
    """Accepts a connection request and stores two parameters,  
    conn which is a socket object for that user, and addr  
    which contains the IP address"""
    conn, addr = server.accept() 
  
    """appends to the list of clients the new client"""
    list_of_clients.append(conn) 
  
    # prints the address of the user that just connected 
    print (addr[0] + " connected")
  
    # creates and individual thread for every user  
    # that connects 
    start_new_thread(clientthread,(conn,addr))     
  
conn.close() 
server.close() 