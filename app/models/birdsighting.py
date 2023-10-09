from flask import session
#from geoalchemy2 import Geometry
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column

from app.models import db, Base

#for login errors
class BirdSightingException(Exception):
    pass

class BirdSighting(Base):
    
    __tablename__ = 'birdsighting'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    bird_id = mapped_column(Integer, ForeignKey('bird.id'), nullable=False)
    timestamp = mapped_column(DateTime, nullable=False)
    #location = mapped_column(Geometry('POINT'))
    notes = mapped_column(String, nullable=True)
    
    def __repr__(self):
        return f'<id: {self.id}, time: {self.timestamp}>'
    
    def __init__(self, bird_id, timestamp, notes):
        self.bird_id = bird_id
        self.timestamp = timestamp
        #self.location = location
        self.notes = notes
    
        
    @staticmethod
    def create(bird_id, timestamp, notes=""):
        pass