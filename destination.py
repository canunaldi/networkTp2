import random
import string
import socket
import time
import threading
import csv

R1_TO_BROKER = '10.10.3.2'
R2_TO_BROKER = '10.10.5.2'



def get_from_r1():
    R1Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    R1Socket.bind((R1_TO_BROKER,3001))
    count = 0
    while 1:
        data,addr = R1Socket.recvfrom(500)
        #print("Num:", count, "len:", len(data))
        print(data)
        count +=1

def get_from_r2():
    R2Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    R2Socket.bind((R2_TO_BROKER,3003))
    count = 0
    while 1:
        data,addr = R2Socket.recvfrom(500)
        #print("Num:", count, "len:", len(data))
        print(data)
        count +=1

th1 = threading.Thread(target=get_from_r1)
th2 = threading.Thread(target=get_from_r2)

th1.start()
th2.start()