'''
Created on 12 Feb 2015

@author: shutebt01
'''

'''
Packet formating:
    [type, src-name, src-group, data]
'''

import socket, threading, json

name = input("Enter User Name: ")
port = 16500
host = input("Enter host: ")
room = "Global"

s = socket.socket()
s.connect((host, port))

class InputThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, target=self.input, name="Thread-Input")
    
    def input(self):
        while True:
            inp = input()
            data = None
            if not(inp.startswith('!')):
                data = json.dumps(["Message", name, room, inp])
            else:
                # Creates initial packet with data for tracking
                packet = ["Event", name, room]
                if inp.startswith("!pm"):
                    split = inp.split(' ', 1)
                    #TODO implement better validation
                    if (len(split) == 2):
                        #Adds data to packet
                        packet[3] = "pm"
                        packet[4] = split[0]
                        packet[5] = split[1]
                data = json.dumps(packet)
            s.send(data.encode("ascii"))

class OutputThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, target=self.output, name="Thread-Output")
        
    def output(self):
        while True:
            data = s.recv(2048).decode("ascii")
            array = json.loads(data)
            if array[0] == "Message":
                print(array[1] + " (" + array[2] + "):" + array[3])
            elif array[0] == "Event":
                if array[3] == "pm":
                    print(array[1] + " (" + array[2] + ") -> You" + array[5])
            
Inp = InputThread()
Inp.start()
Out = OutputThread()
Out.start()
