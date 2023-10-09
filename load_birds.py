from dotenv import load_dotenv
load_dotenv()

from config import Config
from sqlalchemy import create_engine

config = Config()
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, echo=True)

# Now you can create tables based on your models
from app.models import Base

from app.models import Bird
from sqlalchemy.orm import sessionmaker

Session = sessionmaker(bind=engine)
session = Session()

# Delete all rows from the 'bird' table
session.query(Bird).delete()

# Step 1: Read CSV File
import csv
with open('migrations/birds.csv', 'r', encoding='utf-8-sig') as file:
    csv_reader = csv.DictReader(file)
    rows = list(csv_reader)
    
for row in rows:
    bird = Bird(species_code=row['species_code'], common_name=row['common_name'], scientific_name=row['scientific_name'])
    session.add(bird)

session.commit()