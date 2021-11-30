from flask import Blueprint

auth_app = Blueprint(
    'auth',
    __name__,
    url_prefix='/auth'
)

from api.v1.auth.login import *
