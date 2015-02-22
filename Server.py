'''
Created on 10 Feb 2015

@author: shutebt01
'''

import socket, threading, json


s = socket.socket()
host = socket.gethostname()
port = 16500
s.bind((host, port))
s.listen(10)

clients = list()
dats = list()

bannedPhrases = ["", ""]

log = open("Log.log", "a")

with open("Log.log", "a") as myfile:
    myfile.write("\n\n----NEW INIT----\n\n ")

class AcceptThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self, target=self.accept, name="Thread-Accept")
        
    def accept(self):
        while True:
            client, addr = s.accept()
            DT = DataThread(client, addr)
            DT.start()
            dats.append(DT)
            clients.append(client)
            print("Connection from: " + str(addr))
            with open("Log.log", "a") as myfile:
                myfile.write("\nConnection from: " + str(addr))

class DataThread(threading.Thread):
    addr = None
    client = None
    
    def __init__(self, client, addr):
        self.addr = addr
        self.client = client
        threading.Thread.__init__(self, target=self.data, name="Thread-Data-"+str(self.addr))
    
    def data(self):
        while True:
            dat = self.client.recv(2048)
            string = json.loads(dat.decode("ascii"))
            if string[0] == "Message":
                if (string[3] != ""):
                    print("Data (" + dat.decode("ascii") + ")")
                    with open("Log.log", "a") as myfile:
                        myfile.write("\nData: " + dat.decode("ascii"))
                    for c in clients:
                        try:
                            c.send(dat)
                        except:
                            c.close()
            elif string[0] == "Event":
                if (string[3] != ""):
                    print("Data (" + dat.decode("ascii") + ")")
                    with open("Log.log", "a") as myfile:
                        myfile.write("\nData: " + dat.decode("ascii"))
                    for c in clients:
                        try:
                            c.send(dat)
                        except:
                            c.close()
            #except:
                #pass
 
if __name__ == "__main__":               
    Acc = AcceptThread()
    Acc.start()
