#
import sys
import os
import os.path
import socket
import time
import timeit
import getopt
from tempfile import mkstemp
import os
import socket
#import sys
from tlslite.api import *

def clientTestCmd(argv):
    
    address = argv[0]
    #dir = argv[1]    

    #Split address into hostname/port tuple
    address = address.split(":")
    address = ( address[0], int(address[1]) )

    #open synchronisation FIFO
    synchro = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    synchro.settimeout(60)
    synchro.connect((address[0], address[1]-1))

    def connect():
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(15)
        sock.connect(address)
        c = TLSConnection(sock)
        return c

    def testConnClient(conn):
        #user is not finnished
        finnished =False
        
        #while not finnished
        while not finnished:

            #message
            message=input ('enter message:   ')

            data_out= message.encode ()

            #send data out
            conn.write(data_out)    

            #receive data
            data_in=conn.read(1024)

            #decode message
            response= data_in.decode()
            print('Received from client:', response)

            reapet=input('yes or no?  ')

            if reapet == 'n':
                finnished= True
                client_socket.send(b'quit')

    test_no = 0

    badFault = False

    print("Test {0} - anonymous handshake".format(test_no))
    synchro.recv(1)
    connection = connect()
    settings = HandshakeSettings()
    settings.maxVersion = (3, 3)
    connection.handshakeClientAnonymous(settings=settings)
    testConnClient(connection)
    connection.close()

if __name__ == "__main__":
    clientTestCmd(sys.argv[1:])