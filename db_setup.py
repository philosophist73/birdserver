from dotenv import load_dotenv
load_dotenv()

from config import Config
from sqlalchemy import create_engine

config = Config()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)

# Now you can create tables based on your models
from app.models import Base

# Drop all existing tables
Base.metadata.drop_all(engine)

# Create the tables
Base.metadata.create_all(engine)