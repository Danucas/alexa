from flask import Blueprint

restaurants_app = Blueprint(
    'restaurants',
    __name__,
    url_prefix='/restaurants'
)

from api.v1.restaurants.restaurants import *
