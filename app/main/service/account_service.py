import datetime
import jwt
import uuid

from operator import itemgetter
from itertools import groupby
from flask_bcrypt import generate_password_hash, check_password_hash
from app.main import db
from app.main.model.account import Account, Profile, BartleQuotient


def save_new_account(data):
    account = Account.query.filter_by(email=data['email']).first()
    if not account:
        new_user = Account(
            email=data['email'],
            password= generate_password_hash(data['password'], 10),
            created_on=datetime.datetime.utcnow()
        )
        save_changes(new_user)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
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

def login_user(data):
    try:
        account = Account.query.filter_by(email=data['email']).first()
        if account is not None and check_password_hash(account.password, data['password']):      
            token = encode_auth_token(account.id)
            response_object = {
                'status': 'success',
                'message': 'Successfully logged in.',
                'Authorization' : token
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
                'message': 'Try again.',
            }
        return response_object, 401

def encode_auth_token(self, account_id):
    """
    Generates the Auth Token
    :return: string
    """
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),
            'iat': datetime.datetime.utcnow(),
            'sub': account_id
        }
        return jwt.encode(
            payload,
            str(uuid.uuid4()),
            algorithm='HS256'
        )
    except Exception as e:
        return e    

def save_new_bartle_results(data):
    profile = Profile.query.filter_by(account_id=data['account_id'])
    if profile is not None:  
        cnt = len(data['responses'])
        data['responses'].sort(key=itemgetter(1))
        results=groupby(data['responses'],key=itemgetter(1))
        achieverpct=results[1].sum()/cnt
        explorerpct=results[2].sum()/cnt
        killerpct=results[3].sum()/cnt
        socializerpct=results[4].sum()/cnt

        new_bartle_quotient = BartleQuotient(
                profile_id=profile.id,
                achiever_pct=achieverpct,
                explorer_pct=explorerpct ,
                killer_pct=killerpct,   
                socializer_pct=socializerpct   
            )
        
        save_changes(new_bartle_quotient)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Failed to create profile.',
        }
        return response_object, 500

    
# move profile to its own service
def save_new_profile(data):
    profile = Profile.query.filter_by(account_id=data['account_id'])
    if not profile:
        new_profile = Profile(
            account_id=data['account_id'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            friendly_name=data['friendly_name'],
            city=data['city'],
            state=data['state'],
            date_of_birth=data['date_of_birth'],
            skillset_id=data['skillset_id'],
            gender=data['gender']
        )
    
        save_changes(new_profile)
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.',
            'account_id': ""
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Profile already exists.',
        }
        return response_object, 

def update_profile(data):
    profile = Profile.query.filter_by(id=data['id']).first()
    if profile is not None:  
        profile.first_name=data["first_name"]
        profile.last_name=data['last_name']
        profile.friendly_name=data['friendly_name']
        profile.city=data['city']
        profile.state=data['state']
        profile.date_of_birth=data['date_of_birth']
        profile.skillset_id=data['skillset_id']
        profile.gender=data['gender']

        profile.verified = True
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'Successfully registered.'
        }
        return response_object, 201
    else:
        response_object = {
            'status': 'fail',
            'message': 'Profile does not exist.',
        }
        return response_object, 

def get_profile_by_id(account_id):
    return Profile.query.filter_by(id=account_id).first()

def get_all_profiles():
    return Profile.query.all()

def save_changes(data):
    try:
        db.session.add(data)
        db.session.commit()
    except:
        db.session.rollback()

    #db.session.add(data)
    #db.session.commit()