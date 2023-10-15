from flask import session
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column

from app.models import db, Base
from app.models.bird import Bird, BirdException

#for errors
class WatchException(Exception):
    pass

class Watch(Base):
    
    __tablename__ = 'watch'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id = mapped_column(Integer, ForeignKey('account.id'), nullable=False)
    bird_id = mapped_column(Integer, ForeignKey('bird.id'), nullable=False)

    def __repr__(self):
        return f'<account: {self.account_id}, bird: {self.bird_id}>'
    
    def __init__(self, account_id, bird_id):
        self.account_id = account_id
        self.bird_id = bird_id
        
    @staticmethod
    def add(account_id, bird_id):
        try:
            watch = Watch.query.filter_by(account_id=account_id, bird_id=bird_id).first()
            if not watch:

                watch = Watch(
                    account_id=account_id,
                    bird_id=bird_id,
                )

                db.session.add(watch)
                db.session.commit()

            return watch
        except Exception as e:
            raise WatchException(str(e))
        
    @staticmethod
    def remove(account_id, bird_id):
        try:
            watch = Watch.query.filter_by(account_id=account_id, bird_id=bird_id).first()
            if watch:
                db.session.delete(watch)
                db.session.commit()

            return watch
        except Exception as e:
            raise WatchException(str(e))
        
    @staticmethod
    def isWatched(account_id, bird_id):
        try:
            watch = Watch.query.filter_by(account_id=account_id, bird_id=bird_id).first()
            if watch:
                return True
            else:
                return False
        except Exception as e:
            raise Watch(str(e))
        
    @staticmethod
    def getWatchedBirds():
        try:
            watched = Watch.query.filter(Watch.account_id == session["user_id"]).all()
            birds = []
            for watch in watched:
                bird = Bird.getBirdbyID(watch.bird_id)
                birds.append(bird)
            return birds
                
        except Exception as e:
            raise WatchException(str(e))
        