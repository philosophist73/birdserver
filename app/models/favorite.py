from flask import session
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column

from app.models import db, Base
from app.models.bird import Bird, BirdException

#for errors
class FavoriteException(Exception):
    pass

class Favorite(Base):
    
    __tablename__ = 'favorite'
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
            favorite = Favorite.query.filter_by(account_id=account_id, bird_id=bird_id).first()
            if not favorite:

                favorite = Favorite(
                    account_id=account_id,
                    bird_id=bird_id,
                )

                db.session.add(favorite)
                db.session.commit()

            return favorite
        except Exception as e:
            raise FavoriteException(str(e))
        
    @staticmethod
    def remove(account_id, bird_id):
        try:
            favorite = Favorite.query.filter_by(account_id=account_id, bird_id=bird_id).first()
            if favorite:
                db.session.delete(favorite)
                db.session.commit()

            return favorite
        except Exception as e:
            raise FavoriteException(str(e))
        
    @staticmethod
    def isFavorite(account_id, bird_id):
        try:
            favorite = Favorite.query.filter_by(account_id=account_id, bird_id=bird_id).first()
            if favorite:
                return True
            else:
                return False
        except Exception as e:
            raise FavoriteException(str(e))
        
    @staticmethod
    def getFavoriteBirds():
        try:
            favorites = Favorite.query.filter(Favorite.account_id == session["user_id"]).all()
            birds = []
            for favorite in favorites:
                bird = Bird.getBirdbyID(favorite.bird_id)
                birds.append(bird)
            return birds
                
        except Exception as e:
            raise FavoriteException(str(e))
        