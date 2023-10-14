from flask import session
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column

from app.models import db, Base

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
    def create(account_id, bird_id):
        try:
            watch = Watch(
                account_id=account_id,
                bird_id=bird_id,
            )

            db.session.add(watch)
            db.session.commit()

            return watch
        except Exception as e:
            raise WatchException(str(e))