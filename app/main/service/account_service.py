import datetime
import jwt

from flask_bcrypt import generate_password_hash, check_password_hash
from app.main import db
from app.main.model.account import Account

def save_new_account(data):
    account = Account.query.filter_by(email=data['email']).first()
    if not account:
        new_user = Account(
            email=data['email'],
            password= generate_password_hash(data['password'], 10),
            created_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        return generate_token(new_user)

        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'id': new_user.id
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Account already exists. Please Log in.',
        }
        return response_object, 409

def get_all_accounts():
    return Account.query.all()

def get_account_by_id(account_id):
    return Account.query.filter_by(id=account_id).first()

def get_account_by_email(email):
    return Account.query.filter_by(email=email).first()

def generate_token(account: Account):
    try:
        # generate the auth token
        auth_token = Account.encode_auth_token(account.id)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'Authorization': auth_token.decode()
        }
        return response_object, 201
    except Exception as e:
        response_object = {
            'status': 'fail',
            'message': 'Some error occurred. Please try again.'
        }
        return response_object, 401
    
def save_changes(data):
    try:
        db.session.add(data)
        db.session.commit()
    except:
        db.session.rollback()
