import random
import string
import socket
import time
import threading
import csv

R1_TO_BROKER = '10.10.3.2'



def get_from_r1():
    R1Socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    R1Socket.bind((R1_TO_BROKER,3001))
    data,addr = R1Socket.recvfrom(500)
    print(data)

get_from_r1()



