import random
import string
import socket
import time
import threading
from const import *
import csv


result_datas = [] # The resulting end_to_end delays stored in this array

def receive_r1(): # The data receiver that gets the data from R1
    while True: 
        data,addr = R1Socket.recvfrom(18) # The data coming from R1 received and stored into the data variable
        print(data) # Test Issues
        currenttime = time.time() # Time at the destination point
        currenttime = currenttime * 1000 # Similar at the source; this calculation made for preserving the floating points (ms's)
        currenttime = int (currenttime) # To get rid of the unnecessary ms's
        starttime = data[5:] # The starting time came with the data.
        print(data[:4]) # Test issues
        print(starttime) # Test issues
        starttime = int (starttime) # To make calculation starting time converted into an integer value
        end_to_end = currenttime - starttime # end_to_end delay calculation -> Final-Start
        result_datas.append(end_to_end) # Store the delay into the our storage array

        ack = "OK!" # Acknowledge message
        R1Socket.sendto(ack, DEST_TO_R1.get_sender()) # Send acknowledge to R1 (since the data came from R1, R1 waiting for the acknowledge)
        if data[:4] == '3999': # The Last data check (We will print the delays the '3999' point changed manually)
            print("GIRDIM") # Test issues
            with open('result.csv', 'wb') as csvfile: # Open a csv file 
                patcher = csv.writer(csvfile, dialect='excel') # Create csv writer
                patcher.writerow(result_datas) # Write the array into the csv file


# Same work done for R1 at receive_r1 but this time for the data coming from the R2
def receive_r2():
    while True:
        data,addr = R2Socket.recvfrom(18)
        print(data)
        currenttime = time.time()
        currenttime = currenttime * 1000
        currenttime = int (currenttime)
        starttime = data[5:]
        print(data[:4])
        print(starttime)
        starttime = str (starttime)
        starttime = int (starttime)
        end_to_end = currenttime - starttime
        result_datas.append(end_to_end)
        ack = "OK!"
        R2Socket.sendto(ack, DEST_TO_R2.get_sender())
        if data[:4] == '3999':
            with open('result.csv', 'wb') as csvfile:
                patcher = csv.writer(csvfile, dialect='excel')
                patcher.writerow(result_datas)

R1Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # new socket to get the data from R1 and send the acknowledge to R1
R1Socket.bind(R1_TO_DEST.get_listener()) # socket listens R1
R2Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # new socket to get the data from R2 and sends the acknowledge message to the R2
R2Socket.bind(R2_TO_DEST.get_listener()) # socket listens R2
 

# Threads 
th1 = threading.Thread(target= receive_r1, args=()) # A thread that goes to receive_r1 to handle the dataflow between R1 and destination.
th2 = threading.Thread(target= receive_r2, args=()) # Similar thread but this time goes to receive_r2 and the flow between R2 and destination.


#Starting Threads
th1.start()
th2.start()



