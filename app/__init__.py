import imp
from flask import Flask



def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')

    #blueprints imports
    from .views import home_bp
    from .controllers.user import user_bp
    from .controllers.room import room_bp
    from .controllers.hotel import hotel_bp
    from .controllers.auth import auth_bp


    #register blueprint
    app.register_blueprint(home_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(room_bp)
    app.register_blueprint(hotel_bp)
    app.register_blueprint(auth_bp)



    return app