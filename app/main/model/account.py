from .. import db
import datetime
import jwt
from sqlalchemy.sql import func


key = 'goqRfXIYWRmbaqduPaa0Hn7Hf8wzRX0s'
#from flask_bcrypt import Bcrypt


class Account(db.Model):
    """ Account Model for storing user related details """
    __tablename__ = "account"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime,  server_default=func.now())

    
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
