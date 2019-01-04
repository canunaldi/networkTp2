import random
import string
import socket
import time
import threading
import csv
from threading import *
import hashlib



R1_TO_BROKER_recv = '10.10.3.2'
R2_TO_BROKER_recv = '10.10.5.2'

R1_TO_BROKER_send = '10.10.2.1'
R2_TO_BROKER_send = '10.10.4.1'

count = 0
lock = Lock() 
coming_messages = [["0"]*10000] # Resulting message will be created this array. Incoming messages stored here.

def finish():
    result = '' # The data will be collected here.
    i = 0
    indexes = []
    for elem in coming_messages[0]: # For each packet data.
        if '0' in elem: # Test purposes
            indexes.append(i)
        i +=1
        result += elem # Add data to the result.
    with open("result.txt", "w") as f: # Open result.txt in write mode.
        f.write(result) # Write the result to the result.txt.
    print(time.time()) # Print end time for experiments.
    return

def get_from_r1(): # The function that gets the packet from the R1 and sends the acknowledgement to the broker.
    R1Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # new socket for getting data from the broker through R1.
    R1Socket.bind((R1_TO_BROKER_recv,3001)) # Binding
    R1Ack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # new socket for sending Ack to the broker through R1.
    R1Ack.bind((R1_TO_BROKER_recv,3005)) # Binding
    global count
    while 1:
        data,addr = R1Socket.recvfrom(538) # Receive packet sized 538.
        if "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" in data: # If finishing message comes.
            finish() # call finish function
            break
        try:
            index = int(data[500:506]) # Index is the sequence number of the packet.
        except:
            continue
        hashval = data[506:] # Sent Checksum.
        hashvalnew = hashlib.md5(data[:500]).hexdigest() # Calculated checksum

        if str(hashvalnew) == str(hashval): # Checks if they are equal.
            coming_messages[0][index] = data[:500] # Store the data to the comming_messages array's seqnumth part.
            R1Ack.sendto(data[500:506],(R1_TO_BROKER_send,3004)) # Send seqnum as ACK.
        # If not equal do nothing with this packet.
    return

def get_from_r2(): # Note that these are the same calculations made at R1 but just for R2. Therefore you can check the comments above for the corresponding parts.
    R2Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    R2Socket.bind((R2_TO_BROKER_recv,3003))
    R2Ack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    R2Ack.bind((R2_TO_BROKER_recv,3007))
    global count
    while 1:
        data,addr = R2Socket.recvfrom(538)
        if "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" in data:
            finish()
            break
        try:
            index = int(data[500:506])
        except:
            continue
        hashval = data[506:]
        hashvalnew = hashlib.md5(data[:500]).hexdigest()
        if str(hashvalnew) == str(hashval):
            coming_messages[0][index] = data[:500]
            R2Ack.sendto(data[500:506],(R2_TO_BROKER_send,3006))
    return

def deneme(): # Test purposes.
    time.sleep(20)
    result = ''
    i = 0
    indexes = []
    for elem in coming_messages[0]:
        if '0' in elem:
            indexes.append(i)
        i +=1
        result += elem


th1 = threading.Thread(target=get_from_r1) # The threat targetted at get_from_r1
th2 = threading.Thread(target=get_from_r2) # The threat targetted at get_from_r2


# Starting Threads
th1.start()
th2.start()
