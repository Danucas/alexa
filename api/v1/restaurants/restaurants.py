from api.v1.restaurants import restaurants_app
from flask import jsonify, request
from rappi_api import Rappi
from api.v1.utils import get_status, save_status
from threading import Thread


def async_categories(device_id):
    rappi_interface = Rappi(device_id)
    categories = [
        c[1]
        for c in rappi_interface.list_food_categories()
    ]
    save_status(device_id, 'loaded', data=categories)


@restaurants_app.route('/categories', methods=['GET'])
def restaurant_categories():
    device_id = request.args.get('device_id')
    check = request.args.get('check')
    if check:
        if get_status(device_id)['action'] != 'fetching':
            return jsonify(data=get_status(device_id)['data'])
        else:
            return jsonify(data=[])
    else:
        save_status(device_id, 'fetching')
        Thread(target=async_categories, args=(device_id,)).start()
    return jsonify(status='check')


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
