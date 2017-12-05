# Simple Geocoder Service
Written by Jordan Rejaud
For questions/ bug fixes email jrejaud@gmail.com or make a PR/ bug request to Github

## Requirements
Python 2.7.10
[Pipenv](https://docs.pipenv.org/) (for dependencies)

## Installation
1. Clone this repo
2. Use Pipenv (Check Requirements) to install dependencies

## Running the Service
`python server.py`
Server uses port 9000

## Using the Service
Make an HTTP GET call to port 9000 and pass the address you want to as a `location` query  

Example:

`localhost:9000?location=425 Market St, San Francisco, CA, 94105`

Response Format:

```
{
    "latitude": 39.9738534,
    "longitude": -76.60683399999999
}
```

[Postman](https://www.getpostman.com/) is a lovely tool to test out API end points


### Notes
Various TODOs for future changes are in the source code
