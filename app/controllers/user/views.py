from flask import Blueprint

user_bp = Blueprint('user_bp', static_folder='./static', url_prefix='/users', import_name=__name__)


@user_bp.route('/')
def user_home():
    return 'user homepage'