import random
import string
import socket
import time
import threading
from threading import *
import hashlib

SOURCE_TO_BROKER  = '10.10.1.2'
R1_TO_BROKER_bind = '10.10.2.1'
R1_TO_BROKER_send = '10.10.3.2'
R2_TO_BROKER_send = '10.10.5.2'
R2_TO_BROKER_bind = '10.10.4.1'
window_size = 10 # windowsize setted 10
base = 0 # base value
next_seqnum = 0 # next_sequence number
lock = Lock() # lock for locking the problematic parts.
message_list = [] # message_list that stores the data coming from the source.
flag = 0
missing_list = [] # missing_list stores the not received acknowledgements.
timeout = 0 # timeout variable.


def get_message(): # gets the packets from the source
    global flag
    global next_seqnum
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # new socket
    sock.bind((SOURCE_TO_BROKER, 2999)) # Socket listens from the Source
    sock.listen(2) # This socket can listen 2 connection.
    conn, addr = sock.accept() # we get the connection from the source
    while 1:
        data = conn.recv(500,socket.MSG_WAITALL) # Get data from the connection between the source-broker.
        if not data: 
            break
        message_list.append(data) # Append the data to the message_list
    conn.close()

def start_timeout():
    global timeout
    timeout = time.time() # Set timeout variable to the current time.

def wait_timeout():
    global timeout
    left = time.time() -timeout # Calculate the spent time from the starting time until now.
    if 0.05 - left > 0: # If the threshold is passed or not.
        time.sleep(0.05-left) # If not passed wait until threshold value(0.05).



def send(): # Send the data to the destination using r1/r2
    R1Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # new socket
    R1Socket.bind((R1_TO_BROKER_bind, 3000)) # socket binds to the broker side of the link between broker - R1.
    R2Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # new socket
    R2Socket.bind((R2_TO_BROKER_bind, 3002)) # socket binds to the broker side of the link between broker - R2
    global next_seqnum
    global base 
    global missing_list
    count = 0
    while 1:
        if (next_seqnum - base) < 10 and next_seqnum<10000: # If the window size is reached and the next_seqnum is not finished.
            randomvar = random.randint(1,2) # random between the r1,r2
            if randomvar == 1: # go for r1
                lock.acquire() # Lock created since we are changing the missing_list.
                if len(message_list) > next_seqnum: # If check for checking if we are sending faster than the incoming data.
                    seq = str(next_seqnum) # Str version of the next_seqnum
                    while 1:
                        if len(seq) == 6:
                            break
                        seq = "0" + seq # This parts adds zeroes to the start of the next_seqnum until it reaches 6 bytes long.
                    hashval = hashlib.md5(message_list[next_seqnum]).hexdigest() # using hashlib, calculation of the checksum.

                    message = message_list[next_seqnum] + str(seq) + str(hashval) # Creating message Data + Seqnum + Checksum.
                    missing_list.append(next_seqnum)  # Mark the sequence as missing.
                    count +=1
                    R1Socket.sendto(message,(R1_TO_BROKER_send,3001)) # Send it to the dest through R1.
                    next_seqnum +=1 # Increment next_seqnum.
                start_timeout() # Start timeout.
                lock.release()
            else: # Note that these are the same calculations made at R1 but just for R2. Therefore you can check the comments above for the corresponding parts.
                lock.acquire()
                if len(message_list) > next_seqnum:
                    seq = str(next_seqnum)
                    while 1:
                        if len(seq) == 6:
                            break
                        seq = "0" + seq
                    hashval = hashlib.md5(message_list[next_seqnum]).hexdigest()


                    message = message_list[next_seqnum] + str(seq) + str(hashval)
                    missing_list.append(next_seqnum)   
                    count +=1
                    R2Socket.sendto(message,(R2_TO_BROKER_send,3003))
                    next_seqnum +=1
                start_timeout()
                lock.release()
        
        else: # If the window size is reached or the data finished.
            if next_seqnum >= 10000 and missing_list == []: # If the data finished.
                message = ["x"*506] # Send finisher message of xxxxxxxxx...xxx
                R1Socket.sendto(message[0],(R1_TO_BROKER_send,3001))
                R2Socket.sendto(message[0],(R2_TO_BROKER_send,3003))
                R1Socket.sendto(message[0],(R1_TO_BROKER_send,3001))
                R2Socket.sendto(message[0],(R2_TO_BROKER_send,3003))
                R1Socket.sendto(message[0],(R1_TO_BROKER_send,3001))
                R2Socket.sendto(message[0],(R2_TO_BROKER_send,3003))
                R1Socket.sendto(message[0],(R1_TO_BROKER_send,3001))
                R2Socket.sendto(message[0],(R2_TO_BROKER_send,3003))
                R1Socket.sendto(message[0],(R1_TO_BROKER_send,3001))
                R2Socket.sendto(message[0],(R2_TO_BROKER_send,3003))
                R1Socket.sendto(message[0],(R1_TO_BROKER_send,3001))
                R2Socket.sendto(message[0],(R2_TO_BROKER_send,3003))
                R1Socket.sendto(message[0],(R1_TO_BROKER_send,3001))
                R2Socket.sendto(message[0],(R2_TO_BROKER_send,3003))
                R1Socket.sendto(message[0],(R1_TO_BROKER_send,3001))
                R2Socket.sendto(message[0],(R2_TO_BROKER_send,3003))
                R1Socket.sendto(message[0],(R1_TO_BROKER_send,3001))
                R2Socket.sendto(message[0],(R2_TO_BROKER_send,3003))
                R1Socket.sendto(message[0],(R1_TO_BROKER_send,3001))
                R2Socket.sendto(message[0],(R2_TO_BROKER_send,3003))
                while 1:
                    continue
            wait_timeout() # Wait timeout 
            if missing_list != []: # calculate the minimum value from the missing_list.
                minelem = min(missing_list)
            else:
                base = next_seqnum
                continue
            for elem in missing_list: # Loop for the elements at the missing_list.
                randomvar = random.randint(1,2) # Random again for deciding r1/r2.
                if randomvar == 1: # Send to the destination through R1.
                    seq = str(elem) # Str version of the number of the data packet.
                    while 1:
                        if len(seq) == 6:
                            break
                        seq = "0" + seq # The seqnum filled with zeroes until it reached 6 bytes long.
                    base = minelem # base set to the min value.
                    hashval = hashlib.md5(message_list[elem]).hexdigest() # Checksum.

                    message = message_list[elem] + str(seq) + str(hashval) # Message created Data + Seqnum + Checksum
                    R1Socket.sendto(message,(R1_TO_BROKER_send,3001)) # Message sent using R1.
                else: # Note that these are the same calculations made at R1 but just for R2. Therefore you can check the comments above for the corresponding parts.
                    seq = str(elem)
                    while 1:
                        if len(seq) == 6:
                            break
                        seq = "0" + seq
                    base = minelem
                    hashval = hashlib.md5(message_list[elem]).hexdigest()

                    message = message_list[elem] + str(seq) + str(hashval)
                    R2Socket.sendto(message,(R2_TO_BROKER_send,3003))
                start_timeout() # Starting timeout.

            


def get_ack_r1(): # Getting the Acknowledge from the Dest through R1.
    global missing_list
    global base
    R1_ack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # new socket.
    R1_ack.bind((R1_TO_BROKER_bind, 3004)) # Socket binds.
    while 1:
        data,addr = R1_ack.recvfrom(6) # Get the acknowledgement sized 6.
        start_timeout() # Start timeout again.
        data = int(data) # Convert the Acknowledgement to the int value
        lock.acquire() # Lock since we will reach to the missing_list.
        if data in missing_list: # If the data is still in the missing_list, remove it 
            missing_list.remove(data)
        if len(missing_list)>0: # If missing list not empty.
            base = min(missing_list) # Base = minimum of the not acknowledged packet.
        lock.release()

    


    
def get_ack_r2(): # Note that these are the same calculations made at R1 but just for R2. Therefore you can check the comments above for the corresponding parts.
    global missing_list
    global base
    R2_ack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    R2_ack.bind((R2_TO_BROKER_bind, 3006))
    while 1:
        data,addr = R2_ack.recvfrom(6)
        start_timeout()
        data = int(data)
        lock.acquire()
        if data in missing_list:
            missing_list.remove(data)
        if len(missing_list)>0:
            base = min(missing_list)
        lock.release()



broker_listen = threading.Thread(target= get_message, args=()) # Thread targetted get_message function
ack_getter_r1 = threading.Thread(target= get_ack_r1) # Thread targetted get_ack_r1 function
ack_getter_r2 = threading.Thread(target= get_ack_r2) # Thread targetted get_ack_r2 function

broker_listen.start() #Start Thread1
ack_getter_r1.start() #Start Thread2
ack_getter_r2.start() #Start Thread3
send() # Send function starts

