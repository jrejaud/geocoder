#HTTP Server
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

class ServiceHandler(BaseHTTPRequestHandler):
    # Make this the only API endpoint, read the location that the user is passing
    # TODO: How should location be broken up?
    def do_GET(self):
        print "Got HTTP Message!"
        return;

def run(handler_class=ServiceHandler, port=9000):
    server_address = ('', port);
    server = HTTPServer(server_address, handler_class);
    print "Started http server on port: ", port;

    server.serve_forever();


run();
