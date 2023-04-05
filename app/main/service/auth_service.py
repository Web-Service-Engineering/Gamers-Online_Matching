import datetime
import jwt

from flask_bcrypt import check_password_hash
from app.main import db
from app.main.model.account import Account 

key = 'goqRfXIYWRmbaqduPaa0Hn7Hf8wzRX0s'

@staticmethod
def get_logged_in_account(auth_token):
        # get the auth token
       
        if auth_token:
            resp = Account.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                account = Account.query.filter_by(id=resp).first()
                response_object = {
                    'status': 'success',
                    'data': {
                        'account_id': account.id,
                        'email': account.email
                    }
                }
                return response_object, 200
            response_object = {
                'status': 'fail',
                'message': resp
            }
            return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }

            return response_object, 401
        

def login_user(data):

    try:
        account = Account.query.filter_by(email=data['email']).first()
        if account and check_password_hash(account.password, data['password']):      
            token = Account.encode_auth_token(account.id)
            if token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'Authorization': token
                }
            return response_object, 200
        else:
            response_object = {
                'status': 'fail',
                'message': 'Email or password does not match.',
            }
            return response_object, 401
    except Exception as e:
        response_object = {
                'status': 'fail',
                #'message': 'Try again.',
                'message': str(e),
            }
        return response_object, 401

@staticmethod
def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = Account.decode_auth_token(auth_token)
            if not isinstance(resp, str):
                # mark the token as blacklisted
                auth_token = ''
                return auth_token
            else:
                response_object = {
                    'status': 'fail',
                    'message': resp
                }
                return response_object, 401
        else:
            response_object = {
                'status': 'fail',
                'message': 'Provide a valid auth token.'
            }
            return response_object, 403
    
# def encode_auth_token(data):
#     """
#     Generates the Auth Token
#     :return: string
#     """
#     try:
#         payload = {
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5),
#             'iat': datetime.datetime.utcnow(),
#             'sub': data.id
#         }
#         return jwt.encode(
#             payload,
#             key,
#             algorithm='HS256'
#         )
#     except Exception as e:
#         return e    

# def decode_auth_token(auth_token):
#     """
#     Decodes the auth token
#     :param auth_token:
#     :return: integer|string
#     """
#     try:
#         payload = jwt.decode(auth_token, key, algorithms=['HS256'])
        
#         return payload['sub']
#     except jwt.ExpiredSignatureError:
#         return 'Signature expired. Please log in again.'
#     except jwt.InvalidTokenError:
#         return 'Invalid token. Please log in again.'