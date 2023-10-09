from flask import Flask
from flask_session import Session

from app.models import db
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config.get_config())
    db.init_app(app)
    
    # Import and register the blueprint after app and db are defined
    from app.routes import birdserver
    app.register_blueprint(birdserver)

    # Configure session to use filesystem (instead of signed cookies)
    app.config["SESSION_PERMANENT"] = False
    app.config["SESSION_TYPE"] = "filesystem"
    Session(app)
    
    return app

# Optionally, define a __all__ variable to specify which names should be imported when a user does "from package import *"
#__all__ = ['module1', 'module2', 'sub_module1', 'sub_module2', 'my_function']
