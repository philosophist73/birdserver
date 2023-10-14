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
        return f'<Bird (ID: {self.id}, Common Name: {self.common_name}, Species Code: {self.species_code}, Scientific Name: {self.scientific_name})>'
    
    def __init__(self, species_code, common_name, scientific_name):
        self.species_code = species_code
        self.common_name = common_name
        self.scientific_name = scientific_name
    
    @staticmethod
    def search(attr="common_name", bird_name=""):
        if attr == "common_name":
            return Bird.query.filter(Bird.common_name.ilike(f'%{bird_name}%')).all()
        elif attr == "scientific_name":
            return Bird.query.filter(Bird.scientific_name.ilike(f'%{bird_name}%')).all()
        elif attr == "species_code":
            return Bird.query.filter(Bird.species_code.ilike(f'%{bird_name}%')).all()
        else:
            raise BirdException("Invalid attribute")
    
    @staticmethod
    def search_by_common_name(common_name):
        return Bird.query.filter(Bird.common_name == common_name).all()
    
    @staticmethod
    def search_by_scientific_name(scientific_name):
        return Bird.query.filter(Bird.scientific_name == scientific_name).all()
    
    @staticmethod
    def search_by_species_code(species_code):
        return Bird.query.filter(Bird.species_code == species_code).all()
    
    @staticmethod
    def getBirdbyID(bird_id):
        return Bird.query.filter(Bird.id == bird_id).first()