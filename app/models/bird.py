from flask import session
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column

from app.models import db, Base

#for login errors
class BirdException(Exception):
    pass

class Bird(Base):
    
    __tablename__ = 'bird'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    species_code = mapped_column(String, unique=True, nullable=False)
    common_name = mapped_column(String, unique=True, nullable=False)
    scientific_name = mapped_column(String, unique=True, nullable=False)
    
    def __repr__(self):
        return f'<:species_code: {self.species_code}>'
    
    def __init__(self, species_code, common_name, scientific_name):
        self.species_code = species_code
        self.common_name = common_name
        self.scientific_name = scientific_name
    
        
    @staticmethod
    def create(species_code, common_name, scientific_name):
        pass