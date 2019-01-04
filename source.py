from socket import socket, AF_INET, SOCK_STREAM
import time

SOURCE_TO_BROKER = '10.10.1.2' # IP of the link between the source-broker


sock = socket(AF_INET, SOCK_STREAM) # new socket
sock.connect((SOURCE_TO_BROKER, 2999)) # Connects to the link between source and the broker

with open("input.txt", "r") as f: # Opening the input.txt for reading
    print(time.time()) # For experiment, printing the start time.
    for i in range(10000): # 10000 iteration loop for sending the whole data
        message = f.read(500) # Each packet created by reading 500 bytes from the data file
        sock.send(message) # Sending packet to the broker.
