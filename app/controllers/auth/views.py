from flask import Blueprint

auth_bp = Blueprint('auth_bp', static_folder='./static', url_prefix='/auth', import_name=__name__)


@auth_bp.route('/login')
def login():
    return 'login page'