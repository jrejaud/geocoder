#!/usr/bin/env python
# Server
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse

from file import GoogleGeocoder, HereGeocoder

class ServiceHandler(BaseHTTPRequestHandler):
    # Make this the only API endpoint, read the location that the user is passing
    # localhost:9000?location=1234 fake street
    def do_GET(self):
        print "Incoming Get Call"
        location = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('location', None)
        if not location:
            print "User did not provide a location in GET call"
            self.send_response(400)
            self.end_headers()
            return

        # Try to get latLng from Google API
        # response = googleGeocoder.geocodeLocation(location)
        response = hereGeocoder.geocodeLocation(location)

        # If this latLng has errors
        if not response:
            #Hit the other location API
            print("No response")
            self.send_response(500)
            self.end_headers()
            return


        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(response)
        return;

def run(handler_class=ServiceHandler, port=9000):
    server_address = ('', port);
    server = HTTPServer(server_address, handler_class);
    print "Started http server on port: ", port;

    server.serve_forever();

# Create a list of geocoders and iterate through them in order
googleGeocoder = GoogleGeocoder();
hereGeocoder = HereGeocoder();

run();
