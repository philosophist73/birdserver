from flask import session
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.orm import mapped_column
from werkzeug.security import check_password_hash, generate_password_hash

from app.models import db, Base

#for login errors
class AccountException(Exception):
    pass

class Account(Base):
    
    __tablename__ = 'account'
    id = mapped_column(Integer, primary_key=True, autoincrement=True)
    username = mapped_column(String, unique=True, nullable=False)
    password = mapped_column(String, nullable=False)
    
    def __repr__(self):
        return f'<id: {self.id}, username: {self.username}>'
    
    def __init__(self, username, password):
        self.username = username
        self.password = password

    #TODO: dont let two users logs in with same account
    @staticmethod
    def login(username, password):
        
        session.clear()
        
        account = db.session.query(Account).filter(Account.username == username).first()
        if account is not None:
            if check_password_hash(account.password, password):
                #TODO: should this be done in routes instead?
                #TODO: change this to "account id" to match with Account. needs to be updated in routes.py as well
                session["user_id"] = account.id
                return True
        
        raise AccountException("Invalid username and/or password")
    
    @staticmethod
    #TODO: Implement a real logout
    def logout():
        
        session.clear()
        
    @staticmethod
    def create(username, password):
        
        # Check if account already exists
        try:
            account = db.session.query(Account).filter(Account.username == username).first()
        except Exception as e:
            raise AccountException(str(e))
        
        if account is not None:
            raise AccountException("User already exists")
            
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Create account
        try:    
            account = Account(username=username, password=hashed_password)
            db.session.add(account)
            db.session.commit()
            session["user_id"] = account.id
        except Exception as e:
            raise AccountException(str(e))