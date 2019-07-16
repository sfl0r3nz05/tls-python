#client side
# echo client
from socket import *
from ssl import *

def clientTestCmd(argv):

    address = argv[0]
    #dir = argv[1]    

    #Split address into hostname/port tuple
    address = address.split(":")
    address = ( address[0], int(address[1]) )

    #user is not finnished
    finnished =False

    #create socket
    client_socket=socket(AF_INET, SOCK_STREAM)
    tls_client = wrap_socket(client_socket, ssl_version=PROTOCOL_TLSv1, cert_reqs=CERT_NONE)


    #connect to the echo server
    tls_client.connect((address[0], address[1]-1))

    #while not finnished
    while not finnished:

        #message
        message=input ('enter message:   ')

        data_out= message.encode ()

        #send data out
        tls_client.send(data_out)    

        #receive data
        data_in=tls_client.recv(1024)


        #decode message
        response= data_in.decode()
        print('Received from client:', response)

        reapet=input('yes or no?  ')


        if reapet == 'n':
            finnished= True
            client_socket.send(b'quit')



    #close the socket
    client_socket.shutdown(SHUT_RDWR)
    client_socket.close()

if __name__ == "__main__":
    clientTestCmd(sys.argv[1:])
