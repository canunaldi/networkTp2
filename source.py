import random
import string
from socket import socket, AF_INET, SOCK_STREAM
import time
import threading

SOURCE_TO_BROKER = '10.10.1.2'

id = 999 #Packet Id started from 999 -> 1000(will be 1000 in first loop) in order to store Id sized 4 in all packets.
def generate_message(): # Generates message with using Id and current time
    global id
    currtime = time.time() # Current time from the os time
    currtime = currtime * 1000 # Time *1000 in order to not to lose the ms. 
    currtime = int (currtime) # time to integer in order to get rid of the unsused small values
    id +=1 # the id increased for the next packet 
    return "".join(str(id)+ " " + str(currtime)) # Returns "2549 1543765603052" for example Id + Time


sock = socket(AF_INET, SOCK_STREAM) # new socket
sock.connect((SOURCE_TO_BROKER, 3000)) # Connects to the link between source and the broker

with open("dosya.txt", "r") as f:
    for i in range(200):
        message = f.read()
        sock.send(message.encode())
        ack = sock.recv(3)
