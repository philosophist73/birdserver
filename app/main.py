from flask import Flask
from flask_session import Session
from flask_caching import Cache

from app.models import db
from config import Config
from app.routes import register_routes

cache = Cache()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config.get_config())

    cache.init_app(app)
    db.init_app(app)
    register_routes(app)
    Session(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
else:
    gunicorn_app = create_app()