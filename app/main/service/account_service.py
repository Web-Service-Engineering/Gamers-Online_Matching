import datetime
import jwt

from flask_bcrypt import generate_password_hash, check_password_hash
from app.main import db
from app.main.model.account import Account, Profile, BartleQuotient

key = 'goqRfXIYWRmbaqduPaa0Hn7Hf8wzRX0s'

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

@staticmethod
def get_logged_in_account(auth_token):
        # get the auth token
       
        if auth_token:
            resp = decode_auth_token(auth_token)
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
        
@staticmethod
def login_user(data):

    try:
        account = Account.query.filter_by(email=data['email']).first()
        if account and check_password_hash(account.password, data['password']):      
            token = encode_auth_token(account)
            if token:
                response_object = {
                    'status': 'success',
                    'message': 'Successfully logged in.',
                    'Authorization' :  jwt.decode(token, key, algorithms=['HS256'])
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
                'status': 'fail',
                'message': 'Try again.',
            }
        return response_object, 401

@staticmethod
def logout_user(data):
        if data:
            auth_token = data.split(" ")[1]
        else:
            auth_token = ''
        if auth_token:
            resp = decode_auth_token(auth_token)
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
    
def encode_auth_token(data):
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

def decode_auth_token(auth_token):
    """
    Decodes the auth token
    :param auth_token:
    :return: integer|string
    """
    try:
        payload = jwt.decode(auth_token, key, algorithms=['HS256'])
        
        return payload['sub']
    except jwt.ExpiredSignatureError:
        return 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return 'Invalid token. Please log in again.'

def save_new_bartle_results(data):
    profile = Profile.query.filter_by(account_id=data['account_id']).first()

    if profile is not None:  
       
        achiever = data['responses'].count('A')
        explorer = data['responses'].count('E')
        killers = data['responses'].count('K')
        socializer = data['responses'].count('S')
        count = len(data['responses'])

        bartle_quotient = BartleQuotient.query.filter_by(profile_id=profile.id).first()
        if bartle_quotient is None:
            new_bartle_quotient = BartleQuotient(
                    profile_id=profile.id,
                    achiever_pct=achiever/count,
                    explorer_pct=explorer/count ,
                    killer_pct=killers/count,   
                    socializer_pct=socializer/count
                )
        
            save_changes(new_bartle_quotient)
            response_object = {
                'status': 'success',
                'message': 'Successfully created.',
            }
            return response_object, 201
        else:

            bartle_quotient.achiever_pct=achiever/count
            bartle_quotient.explorer_pct=explorer/count 
            bartle_quotient.killer_pct=killers/count 
            bartle_quotient.socializer_pct=socializer/count
            bartle_quotient.verified = True
            db.session.commit()

            response_object = {
                'status': 'success',
                'message': 'Successfully updated.',
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
  
    profile = Profile.query.filter_by(account_id=account_id).first()
    bartle_quotient = BartleQuotient.query.filter_by(profile_id=profile.id).first()
    if bartle_quotient is not None:
        profile.achiever_pct = bartle_quotient.achiever_pct
        profile.explorer_pct = bartle_quotient.explorer_pct
        profile.killer_pct = bartle_quotient.killer_pct
        profile.socializer_pct = bartle_quotient.socializer_pct

    #profile = db.session.query(Profile, BartleQuotient).filter(Profile.id == BartleQuotient.profile_id).filter(account_id==account_id)
    return profile

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