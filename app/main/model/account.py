from .. import db
import datetime
import jwt
from typing import Union

key = 'goqRfXIYWRmbaqduPaa0Hn7Hf8wzRX0s'
#from flask_bcrypt import Bcrypt

class FriendInvitations(db.Model):
    """ FriendInvitations Model for storing friends related details """
    __tablename__ = "friendinvitations"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    account_id = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    account_id_to = db.Column(db.Integer, db.ForeignKey('account.id'), nullable=False)
    created_on = db.Column(db.String(25), nullable=False)

    def __repr__(self) -> int:
        return "<FriendInvitations '{}'>".format(self.id) 

#This is direct translation of the association table 
#This is an auxiliary table that has no data other than the foreign keys
friends = db.Table('friends',
    db.Column('account_id', db.Integer, db.ForeignKey('account.id')),
    db.Column('account_id_to', db.Integer, db.ForeignKey('account.id'))
)

class Account(db.Model):
    """ Account Model for storing user related details """
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.String(25), nullable=False)

    #declare the many-to-many relationship in the users table
    friendships = db.relationship(
        'Account', secondary=friends,
        primaryjoin=(friends.c.account_id == id),
        secondaryjoin=(friends.c.account_id_to == id),
        backref=db.backref('friends', lazy='dynamic'), lazy='dynamic')
    
    def friend(self, account):
        if not self.is_friends(account):
            self.friendships.append(account)

    def unfriend(self, account):
        if self.is_friends(account):
            self.friendships.remove(account)

    def is_friend(self, account):
        return self.friendships.filter(
            friends.c.account_id_to == account.id).count() > 0
    
    def my_friends(self, account):
        return self.friendships.filter(
            friends.c.account_id == account.id).all()
    
  
    
    #@property
    #ref password(self):
      # raise AttributeError('password: write-only field')

    #@password.setter
    #def password(self, password):
      #  self.password_hash = flask_bcrypt.generate_password_hash(password).decode('utf-8')

    #def check_password(self, password):
        #return flask_bcrypt.check_password_hash(self.password_hash, password)

    
    @staticmethod   
    def encode_auth_token(data: int):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
                'iat': datetime.datetime.utcnow(),
                'sub': data.id
            }
            return jwt.encode(
                payload,
                key,
                algorithm='HS256'
            )
        except Exception as e:
            return e  

    @staticmethod   
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key, algorithms=["HS256"])
            
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

  
    def __repr__(self):
        return "<Account '{}'>".format(self.email)  
