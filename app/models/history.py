from flask import session
from sqlalchemy import Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import mapped_column

from app.models import db, Base

#for login errors
class HistoryException(Exception):
    pass

class History(Base):
    
    __tablename__ = 'history'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    account_id = mapped_column(Integer, ForeignKey('account.id'), nullable=False)
    birdsighting_id = mapped_column(Integer, ForeignKey('birdsighting.id'), nullable=False)

    
    def __repr__(self):
        return f'<account: {self.account_id}, birdsighting: {self.birdsighting_id}>'
    
    def __init__(self, account_id, birdsighting_id):
        self.account_id = account_id
        self.birdsighting_id = birdsighting_id
        
    @staticmethod
    def create(account_id, birdsighting_id):
        try:
            history = History(
                account_id=account_id,
                birdsighting_id=birdsighting_id,
            )

            db.session.add(history)
            db.session.commit()

            return history
        except Exception as e:
            raise HistoryException(str(e))