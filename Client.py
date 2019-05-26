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
serverAddr = '127.0.0.1'

clientSocket = socket(AF_INET,SOCK_STREAM)
clientSocket.connect((serverAddr,serverPort))

query = input("Filename to be opened:")

http_query = """
GET /{query} HTTP/1.1
Host: {serverAddr}

"""

clientSocket.send(query.encode('utf-8'))
response = clientSocket.recv(1024).decode('utf-8')

print(response)
clientSocket.close()
