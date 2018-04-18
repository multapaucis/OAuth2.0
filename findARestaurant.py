from geocode import getGeocodeLocation
import json
import httplib2

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)

foursquare_client_id = "L4DGI0NNOHYMQVZFAYJEK4WFIVJVLGWZCQOWTD5Y4EKHECHC"
foursquare_client_secret = "KZYJ2FQSZSJSKFM1A1JFEL4H4A3TZB2BZ3R4OUZIONP1DEYC"


def findARestaurant(mealType,location):
    geoloc = getGeocodeLocation(location)
    ll='%.2f'%geoloc[0]+','+'%.2f'%geoloc[1]
    url = 'https://api.foursquare.com/v2/venues/search?client_id='
    url += '%s&client_secret=%s&v=20130815&ll=%s&radius=100000&intent=browse&limit=1&query=%s' % (foursquare_client_id, foursquare_client_secret, ll, mealType)

    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    if result['response']['venues']:
        venue=result['response']['venues'][0]
        name= venue['name']
        ven_id = venue['id']
        img = getImage(ven_id)
        formaddress = venue['location']['formattedAddress']
        address = ''
        for x in formaddress:
            address += x
            address += ' '
        print 'Name: ' + name
        print 'Address: ' + address
        print 'Image URL: ' + img
        rest_data = {'name':name, 'address':address, 'image': img}
        return rest_data
    else:
        print 'No Restuarant Found'
        return 'No Restuarant Found'

def getImage(ven_id):
    url = 'https://api.foursquare.com/v2/venues/%s/photos?client_id=%s&client_secret=%s&v=20130815' % (ven_id, foursquare_client_id, foursquare_client_secret)
    h = httplib2.Http()
    response, content = h.request(url, 'GET')
    result = json.loads(content)
    if result['response']['photos']['count']==0:
        return 'https://igx.4sqi.net/img/general/300x300/5163668_xXFcZo7sU8aa1ZMhiQ2kIP7NllD48m7qsSwr1mJnFj4.jpg'
    else:
        img_url = ""
        img_url += result['response']['photos']['items'][0]['prefix']
        img_url += '300x300'
        img_url += result['response']['photos']['items'][0]['suffix']
        return img_url
    #1. Use getGeocodeLocation to get the latitude and longitude coordinates of the location string.

    #2.  Use foursquare API to find a nearby restaurant with the latitude, longitude, and mealType strings.
    #HINT: format for url will be something like https://api.foursquare.com/v2/venues/search?client_id=CLIENT_ID&client_secret=CLIENT_SECRET&v=20130815&ll=40.7,-74&query=sushi

    #3. Grab the first restaurant
    #4. Get a  300x300 picture of the restaurant using the venue_id (you can change this by altering the 300x300 value in the URL or replacing it with 'orginal' to get the original picture
    #5. Grab the first image
    #6. If no image is available, insert default a image url
    #7. Return a dictionary containing the restaurant name, address, and image url
if __name__ == '__main__':
    findARestaurant("Pizza", "Tokyo, Japan")
    findARestaurant("Tacos", "Jakarta, Indonesia")
    findARestaurant("Tapas", "Maputo, Mozambique")
    findARestaurant("Falafel", "Cairo, Egypt")
    findARestaurant("Spaghetti", "New Delhi, India")
    findARestaurant("Cappuccino", "Geneva, Switzerland")
    findARestaurant("Sushi", "Los Angeles, California")
    findARestaurant("Steak", "La Paz, Bolivia")
    findARestaurant("Gyros", "Sydney Australia")
