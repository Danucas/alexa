import time

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
    print('Categories loaded from Rappi Frontend')
    print(categories)
    save_status(device_id, 'loaded', data=categories)


@restaurants_app.route('/categories', methods=['GET'])
def restaurant_categories():
    device_id = request.args.get('device_id')
    check = request.args.get('check')
    if check:
        stats = get_status(device_id)
        if 'action' in stats and stats['action'] == 'loaded':
            return jsonify(data=stats['data'])
        else:
            return jsonify(data=[])
    else:
        save_status(device_id, 'fetching', data=[])
        Thread(target=async_categories, args=(device_id,)).start()
    time.sleep(1)
    return jsonify(status='check')


def async_restaurants(device_id, category):
    rappi_interface = Rappi(device_id)
    restaurants = rappi_interface.list_restaurants(category)
    save_status(device_id, 'loaded', data=restaurants)


@restaurants_app.route('/', methods=['GET'])
def restaurants_list():
    device_id = request.args.get('device_id')
    category = request.args.get('category')
    check = request.args.get('check')
    if check:
        stats = get_status(device_id)
        if 'action' in stats and stats['action'] == 'loaded':
            return jsonify(data=stats['data'])
        else:
            return jsonify(data=[])
    else:
        save_status(device_id, 'fetching', data=[])
        Thread(target=async_restaurants, args=(device_id, category,)).start()
    time.sleep(1)
    return jsonify(status='loading')


@restaurants_app.route('/menus', methods=['GET'])
def menu_list():
    device_id = request.args.get('device_id')
    restaurant = request.args.get('restaurant')
    rappi_interface = Rappi(device_id)
    menus = rappi_interface.list_menu_categories(restaurant)
    return jsonify(menus=menus)
