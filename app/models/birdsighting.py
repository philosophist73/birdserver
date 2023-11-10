from flask import session
#from geoalchemy2 import Geometry
from datetime import datetime
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column

from app.models import db, Base

#for login errors
class BirdSightingException(Exception):
    pass

class BirdSighting(Base):
    
    __tablename__ = 'birdsighting'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id = mapped_column(Integer, ForeignKey('account.id'), nullable=False)
    bird_id = mapped_column(Integer, ForeignKey('bird.id'), nullable=False)
    timestamp = mapped_column(DateTime, nullable=False)
    notes = mapped_column(String, nullable=True)
    location = db.Column(String, nullable=True)
    
    def __repr__(self):
        return f'<id: {self.id}, account_id: {self.account_id}, bird_id: {self.bird_id}, timestamp: {self.timestamp}, notes: {self.notes}, location: {self.latitude}>'
    
    def __init__(self, account_id, bird_id, timestamp, notes, location):
        self.account_id = account_id
        self.bird_id = bird_id
        self.timestamp = timestamp
        self.notes = notes
        self.location = location
    
    @staticmethod
    def create(account_id, bird_id, timestamp, notes, location):
        try:
            bird_sighting = BirdSighting(
                account_id=account_id,
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
    
    @staticmethod
    def update(id, timestamp, notes, location):
        try:
            sighting = db.session.query(BirdSighting).filter(BirdSighting.id == id).first()
            #TODO- added this because i was getting this error: SQLite DateTime type only accepts Python datetime and date objects as input 
            sighting.timestamp = datetime.fromisoformat(timestamp)
            sighting.notes = notes
            sighting.location = location

            db.session.commit()
            return sighting            
        except Exception as e:
            raise BirdSightingException(str(e))
        
    @staticmethod
    def getHistory(accountId):
        try:
            sightings = BirdSighting.query.filter(BirdSighting.account_id == accountId).all()
            return sightings
                
        except Exception as e:
            raise BirdSightingException(str(e))
    
    @staticmethod
    def getBirdSightingByID(bird_sighting_id):
        try:
            sightings = BirdSighting.query.filter(BirdSighting.id == bird_sighting_id).all()
            if (sightings is None):
                raise BirdSightingException("No sighting found with id: " + str(bird_sighting_id))
            return sightings[0];
                
        except Exception as e:
            raise BirdSightingException(str(e))