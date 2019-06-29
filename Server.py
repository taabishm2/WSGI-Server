import socket
from io import StringIO
import sys

class WSGIserver(object):

    #IPv4 addressing
    address_family = socket.AF_INET
    #TCP type connection
    socket_type = socket.SOCK_STREAM
    #Request queue size = 1
    request_queue_size = 1

    def __init__(self,server_address):
        #Create a socket listening in
        self.listen_socket = listen_socket = socket.socket(self.address_family, self.socket_type)

        #SOL_SOCKET modifies options for the current socket
        listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        #Assign the IP & Port No.
        listen_socket.bind(server_address)

        #Listen to at most request_queue_size requests
        listen_socket.listen(self.request_queue_size)

        #To obtain server host name & port address
        host,port = self.listen_socket.getsockname()[:2]

        #Get the Fully Qualified Host Name using the host address
        self.server_name = socket.getfqdn(host)
        self.server_port  = port

        #Framework provided header set is saved
        self.header_set = []

    def set_app(self,application):
        self.application = application

    def server_forever(self):

        listen_socket = self.listen_socket

        while True:
            #Establish new client connection
            self.client_connection, client_address = listen_socket.accept()

            #Handle 1 client connection and loop
            self.handle_one_request()

    def handle_one_request(self):
        #Recieve connection request data with 1024 buffer
        self.request_data = request_data = self.client_connection.recv(1024).decode('utf-8')

        #Print out the request data formatted as '< {line}\n'
        print( ''.join( '< {line}\n'.format(line=line) for line in request_data.splitlines() ) )

        #Parse request data sent by client
        self.parse_request(request_data)

        #Returns a dictionary containing WSGI Environment for a request
        env = self.get_environ()

        #Call application and get response to request
        result = self.application(env,self.start_response)

        #Construct reponse and send to client
        self.finish_response(result)

    def parse_request(self,text):
        '''Parse HTTP Request Recieved'''

        #Get the first, request line of HTTP
        request_line = text.splitlines()[0]
        #Remove \r\n of right end
        request_line = request_line.rstrip('\r\n')

        #Split various components of header
        (   self.request_method,    #GET
            self.path,              #/pathname
            self.request_version   #HTTP/1.1
        ) = request_line.split()

    def get_environ(self):
        #WSGI Environment dictionary
        #Contains WSGI info and header info
        env = {}

        #Required WSGI variables
        env['wsgi.version']      = (1, 0)
        env['wsgi.url_scheme']   = 'http'
        env['wsgi.input']        = StringIO(self.request_data)
        env['wsgi.errors']       = sys.stderr
        env['wsgi.multithread']  = False
        env['wsgi.multiprocess'] = False
        env['wsgi.run_once']     = False

        # Required request specific variables
        env['REQUEST_METHOD']    = self.request_method    # GET
        env['PATH_INFO']         = self.path              # /pathname
        env['SERVER_NAME']       = self.server_name       # localhost
        env['SERVER_PORT']       = str(self.server_port)  # 8888
        return env

    def start_response(self, status, response_headers, exc_info=None):

        #Add response header fields here
        server_headers = [
            ('Date', 'Sat, 29 Jun 2019 10:49:12 IST'),
            ('Server', 'WSGIServer 0.2'),
        ]

        #Combined header set of server's response
        self.header_set = [status, response_headers+server_headers]

        #Call function to return finished response
        #return self.finish_response

    def finish_response(self, result):
        try:
            status,response_headers = self.header_set

            #Create HTTP response header line with status
            response = 'HTTP/1.1 {status}\r\n'.format(status=status)

            #Add each header and corresponding value to response
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)

            response += '\r\n'

            #Add results data from application to body
            for data in result:
                response += data.decode('utf-8')

            #Print fomratted response data
            print( ''.join('> {line}\n'.format(line=line) for line in response.splitlines()) )

            #Finally send to client
            self.client_connection.sendall(response.encode('utf-8'))
            print('Sent to client')

        finally:
            self.client_connection.close()
            print('Closed Connection')

def make_server(server_address, application):
    server = WSGIserver(server_address)
    server.set_app(application)
    return server

#Decide IP address and Port address to server.
#Here, we assign local address to server & 8888 is server port
SERVER_ADDRESS = (HOST, PORT) = '', 8888

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.exit('Provide a WSGI application object as module:callable')
    app_path = sys.argv[1]
    module, application = app_path.split(':')

    module = __import__(module)
    print('Imported: ',module)

    application = getattr(module,application)
    print('Obtained application: ',application)

    httpd = make_server(SERVER_ADDRESS, application)
    print("\nWSGIServer: Serving HTTP on port {port} ...\n".format(port=PORT))

    httpd.server_forever()
