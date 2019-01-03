import random
import string
import socket
import time
import threading
from threading import *

SOURCE_TO_BROKER  = '10.10.1.2'
R1_TO_BROKER_bind = '10.10.2.1'
R1_TO_BROKER_send = '10.10.3.2'
R2_TO_BROKER_send = '10.10.5.2'
R2_TO_BROKER_bind = '10.10.4.1'
window_size = 10
base = 0
next_seqnum = 0
lock = Lock()
message_list = []
flag = 0
def get_message():
    global flag
    global next_seqnum
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # new socket
    sock.bind((SOURCE_TO_BROKER, 2999)) # Socket listens from the Source
    sock.listen(2) # This socket can listen 2 connection.
    conn, addr = sock.accept() # we get the connection from the source
    count = 0
    while 1:
        data = conn.recv(500,socket.MSG_WAITALL).decode()
        if not data:
            break
        lock.acquire()
        print("ML:",count, " len:",len(data))
        message_list.append(data)
        lock.release()
        count +=1
        #print(data)
    conn.close()


def send():
    R1Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    R1Socket.bind((R1_TO_BROKER_bind, 3000))
    R2Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    R2Socket.bind((R2_TO_BROKER_bind, 3002))
    global next_seqnum
    count = 0
    while 1:
        randomvar = random.randint(1,2)
        if randomvar == 1:
            lock.acquire()
            if len(message_list) > next_seqnum:
                #print("ML: ",len(message_list)) 
                #print("NSq:", next_seqnum)
                print("Send:", next_seqnum, " len:",len(message_list[next_seqnum]))  
                count +=1
                R1Socket.sendto(message_list[next_seqnum],(R1_TO_BROKER_send,3001))
                next_seqnum +=1
                time.sleep(0.2)
            lock.release()
        else:
            lock.acquire()
            if len(message_list) > next_seqnum:
                #print("ML: ",len(message_list)) 
                #print("NSq:", next_seqnum)
                print("Send:", next_seqnum, " len:",len(message_list[next_seqnum]))  
                count +=1
                R1Socket.sendto(message_list[next_seqnum],(R2_TO_BROKER_send,3003))
                next_seqnum +=1
                time.sleep(0.2)
            lock.release()



broker_listen = threading.Thread(target= get_message, args=())
broker_listen.start()
send()




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


    

