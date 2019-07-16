#server side
# echo client
from socket import *
from ssl import *

def serverTestCmd(argv):

    address = argv[0]
    dir = argv[1]
    
    #Split address into hostname/port tuple
    address = address.split(":")
    address = ( address[0], int(address[1]) )

    #create socket
    server_socket=socket(AF_INET, SOCK_STREAM)

    #Bind to an unused port on the local machine
    server_socket.bind((address[0], address[1]-1))

    #listen for connection
    server_socket.listen (1)
    tls_server = wrap_socket(server_socket, ssl_version=PROTOCOL_TLSv1, cert_reqs=CERT_NONE, server_side=True, keyfile='../../tlslite-ng/tests/serverX509Key.pem', certfile='../../tlslite-ng/tests/serverX509Cert.pem')

    print('server started')

    #accept connection
    connection, client_address= tls_server.accept()
    print ('connection from', client_address)

    #server is not finnished
    finnished =False

    #while not finnished
    while not finnished:


        #send and receive data from the client socket
        data_in=connection.recv(1024)
        message=data_in.decode()
        print('client send',message)

        if message=='quit':
            finnished= True
        else:

            data_out=message.encode()
            connection.send(data_out)

    #close the connection
    connection.shutdown(SHUT_RDWR)
    connection.close()

    #close the server socket
    server_socket.shutdown(SHUT_RDWR)
    server_socket.close()

if __name__ == "__main__":
    serverTestCmd(sys.argv[1:])