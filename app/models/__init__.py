from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
db = SQLAlchemy(model_class=Base)

from app.models.account import Account
from app.models.bird import Bird
from app.models.birdsighting import BirdSighting
from app.models.favorite import Favorite
from app.models.watch import Watch
