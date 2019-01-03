import random
import string
import socket
import time
import threading
import csv
from threading import *


R1_TO_BROKER_recv = '10.10.3.2'
R2_TO_BROKER_recv = '10.10.5.2'

R1_TO_BROKER_send = '10.10.2.1'
R2_TO_BROKER_send = '10.10.4.1'

count = 0
lock = Lock()
coming_messages = [["0"]*200]


def get_from_r1():
    R1Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    R1Socket.bind((R1_TO_BROKER_recv,3001))
    R1Ack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    R1Ack.bind((R1_TO_BROKER_recv,3005))
    global count
    while 1:
        data,addr = R1Socket.recvfrom(506)
        #print("Num:", count, "len:", len(data))
        index = int(data[500:])
        coming_messages[0][index] = data[:500]
        R1Ack.sendto(data[500:],(R1_TO_BROKER_send,3004))

def get_from_r2():
    R2Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    R2Socket.bind((R2_TO_BROKER_recv,3003))
    R2Ack = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    R2Ack.bind((R2_TO_BROKER_recv,3007))
    global count
    while 1:
        data,addr = R2Socket.recvfrom(506)
        #print("Num:", count, "len:", len(data))
        index = int(data[500:])
        coming_messages[0][index] = data[:500]
        R2Ack.sendto(data[500:],(R2_TO_BROKER_send,3006))

def deneme():
    time.sleep(10)
    print(coming_messages)


th1 = threading.Thread(target=get_from_r1)
th2 = threading.Thread(target=get_from_r2)

th1.start()
th2.start()
deneme()
