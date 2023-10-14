from flask import session
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column

from app.models import db, Base

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
    def create(account_id, bird_id):
        try:
            favorite = Favorite(
                account_id=account_id,
                bird_id=bird_id,
            )

            db.session.add(favorite)
            db.session.commit()

            return favorite
        except Exception as e:
            raise FavoriteException(str(e))