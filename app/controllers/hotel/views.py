from flask import Blueprint

hotel_bp = Blueprint('hotel_bp', static_folder='./static', url_prefix='/hotels', import_name=__name__)


@hotel_bp.route('/')
def hotel_home():
    return 'hotel homepage'