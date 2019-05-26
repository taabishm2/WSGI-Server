from socket import *
from http.server import BaseHTTPRequestHandler
from io import StringIO

#For parsing HTTP Requests
class HTTPRequest(BaseHTTPRequestHandler):
    def __init__(self, request_text):
        self.rfile = StringIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()

    def send_error(self, code, message):
        self.error_code = code
        self.error_message = message

serverPort = 8080
serverSocket = socket(AF_INET,SOCK_STREAM)  #Set up a IPv4 system using TCP Protocol

serverSocket.bind(('',serverPort))  #Bind the port number to current server application

serverSocket.listen(1)  #Listens to incoming connections with a maximum of 1 connections in queue
print("Server running...")

for i in range (3):    #Server always keeps running
    connectionSocket,addr = serverSocket.accept()   #Performs 3 way handshake. Sockets are set up per each connection in TCP as multiplexing involves source IP & Port No.
    request = connectionSocket.recv(1024)    #Receive the request from client. Buffer of 1024

    #Parsing the request HTTP
    request = request.decode('utf-8')
    request = HTTPRequest(request)
    
    fname = request.path

    try:
        fp = open(fname,mode='r')
        fp = fp.read()
        response = fp.encode('utf-8')

        response = f"""\
HTTP/1.1 200 OK

<h1>{response}</h1>
"""
    except:
        response = f"""\
HTTP/1.1 404 Not Found

"""
        
    connectionSocket.sendall(response.encode('utf-8'))
    connectionSocket.close()
    
