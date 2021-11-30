from api.v1.restaurants import restaurants_app
from flask import jsonify, request
from rappi_api import Rappi
import json
import os
import time


@restaurants_app.route('/categories', methods=['GET'])
def restaurant_categories():
    device_id = request.args.get('device_id')
    rappi_interface = Rappi(device_id)
    categories = [
        c[1]
        for c in rappi_interface.list_food_categories()
    ]
    return jsonify(categories=categories)


@restaurants_app.route('/', methods=['GET'])
def restaurants_list():
    device_id = request.args.get('device_id')
    category = request.args.get('category')
    rappi_interface = Rappi(device_id)
    restaurants = rappi_interface.list_restaurants(category)
    return jsonify(restaurants=restaurants)


@restaurants_app.route('/menus', methods=['GET'])
def menu_list():
    device_id = request.args.get('device_id')
    restaurant = request.args.get('restaurant')
    rappi_interface = Rappi(device_id)
    menus = rappi_interface.list_menu_categories(restaurant)
    return jsonify(menus=menus)
