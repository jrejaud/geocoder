#!/usr/bin/env python
from abc import ABCMeta, abstractmethod
import requests, json

class Geocoder(object):
    """Abstract Geocoder class.
    Inherit this class for whatever
    3rd party geocoding you want to use."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def geocodeLocation(self, location):
        pass

    # Validate that the address is correct
    def validateAddress(self, location):
        # TODO Implement this function
        return True

class GoogleGeocoder(Geocoder):

    # TODO Move this key to a more secure location (system envs) as opposed to just keeping it in source
    API_KEY = "AIzaSyBnM9ABU-ahZz-5_U0rEkeUCx6pD7lQ-zU";
    BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

    def geocodeLocation(self, location):
        if not self.validateAddress(location):
            #return "Invalid address"
            return False
        print "Geting Location from Google's API"
        payload = {"address": location, "key": self.API_KEY}
        # This is synchronous, it will not scale once many users are hitting the server at once.
        r = requests.get(self.BASE_URL, payload)
        # Check if response is valid
        if not r.status_code == 200:
            #return "Invalid response"
            return False

        # TODO Check to make sure the json response is in this format
        latLng = r.json()["results"][0]["geometry"]["location"]
        print "Got latLng from Google ", latLng

        # Construct a response
        return json.dumps({"latitude":latLng["lat"], "longitude":latLng["lng"]})


class HereGeocoder(Geocoder):

    # TODO Move this key to a more secure location (system envs) as opposed to just keeping it in source
    APP_ID = "SBeLfuAJ24jrljc0zYER"
    APP_CODE = "VZpVZDanVRLoVNIHj4PObA"
    BASE_URL = "https://geocoder.cit.api.here.com/6.2/geocode.json"

    def geocodeLocation(self, location):
        if not self.validateAddress(location):
            return "Invalid address"
            return False
        print "Getting Location from Geocoder API"
        payload = {"app_id": self.APP_ID, "app_code": self.APP_CODE, "searchtext": location}
        # This is synchronous, it will not scale once many users are hitting the server at once.
        r = requests.get(self.BASE_URL, payload)
        # Check if response is valid
        if not r.status_code == 200:
            return "Invalid response"
            return False

        # TODO Check to make sure the json response is in this format
        latLng = r.json()["Response"]["View"][0]["Result"][0]["Location"]["DisplayPosition"]
        print "Got latLng from Geocoder ", latLng

        # Construct a response
        return json.dumps({"latitude":latLng["Latitude"], "longitude":latLng["Longitude"]})
