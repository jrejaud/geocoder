#!/usr/bin/env python
# Server
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import urlparse

from geocoders import GoogleGeocoder, HereGeocoder

class ServiceHandler(BaseHTTPRequestHandler):
    # Make this the only API endpoint, read the location that the user is passing
    def do_GET(self):
        print "Incoming Get Call"
        location = urlparse.parse_qs(urlparse.urlparse(self.path).query).get('location', None)

        # Try to get latLng from the Geocoders in the list
        response = None

        for geocoder in geocoders:
            # Try to get a response from a geocoder
            response = geocoder.geocodeLocation(location)
            # If you get an invalid address, break out of the loop
            if response[0] == 1:
                break
            # If you manage to get positive response, break out of the loop
            if response[0] == 0:
                break

        print response

        # If the user provided a bad address
        if response[0] == 1:
            self.send_response(400)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(response[1])
            return

        # If you got a bad response from the external APIs
        if response[0] != 0:
            self.send_response(500)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write(response[1])
            return

        # Return the geocoding lat/lng response
        self.send_response(200)
        self.send_header('Content-type','application/json')
        self.end_headers()
        self.wfile.write(response)
        return;

def run(handler_class=ServiceHandler, port=9000):
    # TODO Add some sort of authentication so randos/ bots don't hit this end point
    server_address = ('', port);
    server = HTTPServer(server_address, handler_class);
    print "Started http server on port: ", port;
    print "Now ready to geocode your locations!"

    server.serve_forever();

# Create a list of geocoders and iterate through them in order
geocoders = [GoogleGeocoder(), HereGeocoder()]

# TODO Change the geocoders based on passed parameters

run();
