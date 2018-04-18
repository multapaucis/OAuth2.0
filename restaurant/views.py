from findARestaurant import findARestaurant
from models import Base, Restaurant
from flask import Flask, jsonify, request, redirect, url_for
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
sys.stdout = codecs.getwriter('utf8')(sys.stdout)
sys.stderr = codecs.getwriter('utf8')(sys.stderr)




#foursquare_client_id = ''

#foursquare_client_secret = ''

#google_api_key = ''

engine = create_engine('sqlite:///restaruants.db')

Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
app = Flask(__name__)

@app.route('/restaurants', methods = ['GET', 'POST'])
def all_restaurants_handler():
    if request.method == 'POST':
        meal = request.args.get('mealType', '')
        location = request.args.get('location', '')
        restaurant = findARestaurant(meal, location)
        newRestaurant = Restaurant(
                                    restaurant_name=restaurant['name'],
                                    restaurant_address=restaurant['address'],
                                    restaurant_image=restaurant['image']
                                    )
        session.add(newRestaurant)
        session.commit()
        return jsonify(newRestaurant=newRestaurant.serialize)
    if request.method == 'GET':
        restaurants = session.query(Restaurant).all()
        return jsonify(restaurants=[r.serialize for r in restaurants])


@app.route('/restaurants/<int:id>', methods = ['GET','PUT', 'DELETE'])
def restaurant_handler(id):
    restaurant = session.query(Restaurant).filter_by(id=id).one()
    if request.method == 'GET':
        return jsonify(restaurant=restaurant.serialize)
    if request.method == 'PUT':
        if request.args.get('name', ''):
            restaurant.restaurant_name= request.args.get('name')
        if request.args.get('location', ''):
            restaurant.restaurant_address = request.args.get('location')
        if request.args.get('image', ''):
            restaurant.restaurant_image = request.args.get('image')
        session.add(restaurant)
        session.commit()
        return jsonify(restaurant=restaurant.serialize)
    if request.method == 'DELETE':
        session.delete(restaurant)
        session.commit()
        return 'Restaurant has been Deleted'


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=5000)



