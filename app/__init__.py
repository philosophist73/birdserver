from flask import Flask
from flask_session import Session
from flask_caching import Cache

from app.models import db
from config import Config

cache = Cache()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config.get_config())
    cache.init_app(app)
    db.init_app(app)
    
    # Import and register the blueprint after app and db are defined
    from app.routes import birdserver
    app.register_blueprint(birdserver)

    # Configure HTTP session
    Session(app)
    
    return app