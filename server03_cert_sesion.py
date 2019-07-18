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

def serverTestCmd(argv):

    address = argv[0]
    dir = argv[1]
    
    #Split address into hostname/port tuple
    address = address.split(":")
    address = ( address[0], int(address[1]) )

    #Create synchronisation FIFO
    synchroSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    synchroSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    synchroSocket.bind((address[0], address[1]-1))
    synchroSocket.listen(2)

    #Connect to server
    lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    lsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    lsock.bind(address)
    lsock.listen(5)

    # following is blocking until the other side doesn't open
    synchro = synchroSocket.accept()[0]

    def connect():
        s = lsock.accept()[0]
        s.settimeout(15)
        return TLSConnection(s)

    def testConnServer(connection):
        finnished =False
        while not finnished:
            #send and receive data from the client socket
            data_in=connection.read(1024)
            message=data_in.decode()
            print('client send',message)
            
            if message=='quit':
                finnished= True
            else:
                data_out=message.encode()
                connection.write(data_out)

    x509Cert = X509().parse(open(os.path.join(dir, "serverX509Cert.pem")).read())
    x509Chain = X509CertChain([x509Cert])
    s = open(os.path.join(dir, "serverX509Key.pem")).read()
    x509Key = parsePEMKey(s, private=True)

    with open(os.path.join(dir, "serverRSAPSSSigCert.pem")) as f:
        x509CertRSAPSSSig = X509().parse(f.read())
    x509ChainRSAPSSSig = X509CertChain([x509CertRSAPSSSig])
    with open(os.path.join(dir, "serverRSAPSSSigKey.pem")) as f:
        x509KeyRSAPSSSig = parsePEMKey(f.read(), private=True)

    with open(os.path.join(dir, "serverRSAPSSCert.pem")) as f:
        x509CertRSAPSS = X509().parse(f.read())
    x509ChainRSAPSS = X509CertChain([x509CertRSAPSS])
    assert x509CertRSAPSS.certAlg == "rsa-pss"
    with open(os.path.join(dir, "serverRSAPSSKey.pem")) as f:
        x509KeyRSAPSS = parsePEMKey(f.read(), private=True,
                                    implementations=["python"])

    test_no = 0
    
    print("Test {0} - good X.509 (plus SNI)".format(test_no))
    synchro.send(b'R')
    connection = connect()
    connection.handshakeServer(certChain=x509Chain, privateKey=x509Key)
    assert connection.session.serverName == address[0]
    assert connection.extendedMasterSecret
    assert connection.session.appProto is None
    testConnServer(connection)
    connection.close()


if __name__ == "__main__":
    serverTestCmd(sys.argv[1:])