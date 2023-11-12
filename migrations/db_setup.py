from dotenv import load_dotenv
load_dotenv('.flaskenv')

from config import Config
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database

config = Config()
#BUG: hard coded to directory for now (./sqlite)
engine = create_engine("sqlite:///./sqlite/birdserver.db", echo=True)
if not database_exists(engine.url): create_database(engine.url)

# Now you can create tables based on your models
from app.models import Base

# Drop all existing tables
Base.metadata.drop_all(engine)

# Create the tables
Base.metadata.create_all(engine)