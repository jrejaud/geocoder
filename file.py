#!/usr/bin/env python
from abc import ABCMeta, abstractmethod

class Geocoder(object):
    """Abstract Geocoder class.
    Inherit this class for whatever
    3rd party geocoding you want to use."""
    __metaclass__ = ABCMeta

    @abstractmethod
    def geocodeLocation(self, location):
        pass


class GoogleGeocoder(Geocoder):
    def geocodeLocation(self, location):
        print "Get Location from Google!";


# Implement this later
class SecondGeocoder(Geocoder):
    def geocodeLocation(self, location):
        print "Get Location from a second API";



x = GoogleGeocoder();
x.geocodeLocation("sa");
