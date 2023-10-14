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
    notes = mapped_column(String, nullable=True)
    location = db.Column(String, nullable=True)
    
    def __repr__(self):
        return f'<id: {self.id}, bird_id: {self.bird_id}, timestamp: {self.timestamp}, notes: {self.notes}, location: {self.latitude}>'
    
    def __init__(self, bird_id, timestamp, notes, location):
        self.bird_id = bird_id
        self.timestamp = timestamp
        self.notes = notes
        self.location = location
    
    @staticmethod
    def create(bird_id, timestamp, notes, location):
        try:
            bird_sighting = BirdSighting(
                bird_id=bird_id,
                timestamp=timestamp,
                notes=notes,
                location=location
            )

            db.session.add(bird_sighting)
            db.session.commit()

            return bird_sighting
        except Exception as e:
            raise BirdSightingException(str(e))