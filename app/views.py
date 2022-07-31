from flask import Blueprint
from . import User


home_bp = Blueprint('home_bp', static_folder='./static', url_prefix='/', import_name=__name__)

@home_bp.route('/')
def home():
    new_user = User(
                first_name='Hyelda',
                last_name='Dzarma',
                phone_num='08033333862',
                address='Yola',
                email='hndzarma@gmail.com',
                password='password',
                hotel_id=None,
                role_id=None
            )

    new_user.insert()

    return new_user.format()