from flask import Blueprint


home_bp = Blueprint('home_bp', static_folder='./static', url_prefix='/', import_name=__name__)

@home_bp.route('/')
def home():
    return 'main homepage'