import httplib2
import json

def getGeocodeLocation(inputString):
    google_api_key = 'AIzaSyC3p-98q4xnYV6_zQSx9OKqPvnvg08n-OU'
    location_string = inputString.replace(" ", "+")
    url = (
        'https://maps.googleapis.com/maps/api/geocode/json?address=%s&key=%s'
         % (location_string, google_api_key))
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    #print 'Response Header: %s \n \n' % response
    latitude = result['results'][0]['geometry']['location']['lat']
    longitude = result['results'][0]['geometry']['location']['lng']
    return (latitude,longitude)
