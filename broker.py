import random
import string
import socket
import time
import threading

print("2")
SOURCE_TO_BROKER = '10.10.1.2'

message_list = []

def get_message():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # new socket
    sock.bind((SOURCE_TO_BROKER, 3000)) # Socket listens from the Source
    sock.listen(2) # This socket can listen 2 connection.
    conn, addr = sock.accept() # we get the connection from the source 
    count = 0
    while 1:
        data = conn.recv(500).decode()
        if not data:
            break
        #print(data)
        message_list.append(data)
        count +=1
        if count == 195:
            print(message_list)
    conn.close()



broker_listen = threading.Thread(target= get_message, args=())
broker_listen.start()



#random = 0  # To decide where to send the next packet R1 or R2
#sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # new socket
#sock.bind(SOURCE_TO_BROKER.get_listener()) # Socket listens from the Source
#sock.listen(2) # This socket can listen 2 connection. 
#conn, addr = sock.accept() # we get the connection from the source 
#R1Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # new socket in order to get the acknowledge from the R1 and send to R1
#R1Socket.bind(R1_TO_BROKER.get_sender()) # binds to R1 in order to acquire acknowledge
#R2Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # new socket in order to get the acknowledge from the R2 and send to R2
#R2Socket.bind(R2_TO_BROKER.get_sender()) # binds to R2 in order to acquire acknowledge
#while 1: # inf loop
#    data = conn.recv(18).decode() # gets data coming from the source
#    if not data: # This if statement checks if the source stoped sending message ie. the message is empty
#        break
#    print "received data:", data # Test issues
#    if random == 0: # We send packet to the R1 
#        R1Socket.sendto(data, BROKER_TO_R1.get_listener()) # Using socket2 in order to send the data to the R1
#        random = 1  # Change the random variable to send the next packet to R2
#        ack,addr = R1Socket.recvfrom(3) # Get the acknowledge from the R1
#        conn.send(ack) #Send the acknowledge to the Source
#        print(ack) # Test issues

#   elif random == 1: # Now send packet to the R2
#        R2Socket.sendto(data, BROKER_TO_R2.get_listener()) #  Using socket3 in order to send the data to the R2
#        random = 0  # Change the random variable to send the next packet to R1
#        ack,addr = R2Socket.recvfrom(3) # Get the acknowledge from the R2
#        conn.send(ack) # Send the acknowledge to the Source
#        print(ack) # Test issues


    
