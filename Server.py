import socket

#Decide IP address and Port address to server.
#Here, we assign local address to server & 8888 is server port
serverAddr,serverPort = '', 8888

#Create a socket interface.
#AF_INET indicates IPv4 addressing, SOCK_STREAM implies UDP Connection
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Setting Socket options
#SOL_SOCKET modifies options for the current socket
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

#Assign the IP & Port No.
serverSocket.bind((serverAddr,serverPort))

#Enable requests to server
serverSocket.listen(1)


print("Server running on Port:",serverPort)
