#!/usr/bin/env python
from abc import ABCMeta, abstractmethod
import requests, json

# Geocoders
class Geocoder(object):
    """Abstract Geocoder class.
    Inherit this class for whatever
    3rd party geocoding you want to use."""
    __metaclass__ = ABCMeta

    # Return a JSON location, or one of the following integers:
    # 0: No errors
    # 1: User provided an invalid address
    # 2: 3rd party geolocating service provided a bad response (status code != 200)
    # 3: 3rd party JSON response is not formatted properly
    @abstractmethod
    def geocodeLocation(self, location):
        pass

    # Validate that the address is correct
    # This is currently run once per geocoder, eventually make it run only once per GET
    def validateAddress(self, location):
        # TODO Implement a more robust version of this function

        # Check if the string is null or is empty
        if not location:
            return False

        return True


class GoogleGeocoder(Geocoder):

    # TODO Move this key to a more secure location (system envs) as opposed to just keeping it in source
    API_KEY = "AIzaSyBnM9ABU-ahZz-5_U0rEkeUCx6pD7lQ-zU";
    BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

    def geocodeLocation(self, location):
        if not self.validateAddress(location):
            # Invalid Address
            return [1, "Invalid user provided address"]
        print "Trying to get location from Google's API"
        payload = {"address": location, "key": self.API_KEY}
        # This is synchronous, it will not scale once many users are hitting the server at once.
        r = requests.get(self.BASE_URL, payload)
        # Check if response is valid
        if not r.status_code == 200:
            # Invalid response
            return [2, "Invalid Response from external geocoding service"]

        #Check to make sure the json response is in this format
        try:
            latLng = r.json()["results"][0]["geometry"]["location"]
        except:
            # Bad JSON Response
            return [3, "Bad JSON Response from external server"]

        print "Got latLng from Google ", latLng

        # Construct a response
        return [0, json.dumps({"latitude":latLng["lat"], "longitude":latLng["lng"]})]


class HereGeocoder(Geocoder):

    # TODO Move these keys to a more secure location (system envs) as opposed to just keeping it in source
    APP_ID = "SBeLfuAJ24jrljc0zYER"
    APP_CODE = "VZpVZDanVRLoVNIHj4PObA"
    BASE_URL = "https://geocoder.cit.api.here.com/6.2/geocode.json"

    def geocodeLocation(self, location):
        if not self.validateAddress(location):
            # Invalid Address
            return [2, "Invalid user provided address"]
        print "Trying to get location from Geocoder's API"
        payload = {"app_id": self.APP_ID, "app_code": self.APP_CODE, "searchtext": location}
        # This is synchronous, it will not scale once many users are hitting the server at once.
        r = requests.get(self.BASE_URL, payload)
        # Check if response is valid
        if not r.status_code == 200:
            # Invalid response
            return [2, "Invalid Response from external geocoding service"]

        # Check to make sure the json response is in this format
        try:
            latLng = r.json()["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]
        except:
            # Bad JSON Response
            return [3, "Bad JSON Response from external geocoding service"]

        print "Got latLng from Geocoder ", latLng

        # Construct a response
        return [0, json.dumps({"latitude":latLng["Latitude"], "longitude":latLng["Longitude"]})]
