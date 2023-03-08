import datetime
from flask_bcrypt import generate_password_hash, check_password_hash

from app.main import db
from app.main.model.account import Account, Profile


def save_new_account(data):
    account = Account.query.filter_by(email=data['email']).first()
    if not account:
        new_user = Account(
            email=data['email'],
            password= generate_password_hash(data['password']),
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

def save_new_profile(data):
    profile = Profile.query.filter_by(account_id=data['account_id']).first()
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