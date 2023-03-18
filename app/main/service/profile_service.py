import datetime

from app.main import db
from app.main.model.profile import Profile, BartleQuotient


def save_new_bartle_results(data):
    profile = Profile.query.filter_by(account_id=data['account_id']).first()

    if profile:         
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
            'message': 'Failed to store bartle test results.',
        }
        return response_object, 500
   
# move profile to its own service
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
            'account_id': data['account_id']
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

def get_profile_by_id(data):
    id = data
    profile = Profile.query.filter_by(account_id=id).first()
    if profile is not  None:
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