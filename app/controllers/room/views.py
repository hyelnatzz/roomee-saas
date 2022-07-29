from flask import Blueprint


room_bp = Blueprint('room_bp', static_folder='./static', url_prefix='/rooms', import_name=__name__)

@room_bp.route('/')
def room_home():
    return 'room homepage'