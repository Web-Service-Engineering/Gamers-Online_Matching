import datetime

from sqlalchemy.sql import exists
from app.main import db
from app.main.model.profile import Profile, BartleQuotient, Friends, ProfileFriendship, FriendshipInvitations

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
                    achiever_pct=(achiever/count) * 2,
                    explorer_pct=(explorer/count) * 2,
                    killer_pct=(killers/count) * 2,   
                    socializer_pct=(socializer/count) * 2
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
            'profile_id': new_profile.id,
            'account_id': new_profile.account_id
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
    #results = db.session.query(BartleQuotient, Profile).join(BartleQuotient, Profile.id == BartleQuotient.profile_id, isouter=True).filter(Profile.account_id==id).first()
    #profile = results.Profile
    if profile is not  None:
        bartle_quotient = BartleQuotient.query.filter_by(profile_id=profile.id).first()
       #if results.BartleQuotient is not None:
        if bartle_quotient is not None:
            #bartle_quotient = results.BartleQuotient
            profile.achiever_pct = bartle_quotient.achiever_pct
            profile.explorer_pct = bartle_quotient.explorer_pct
            profile.killer_pct = bartle_quotient.killer_pct
            profile.socializer_pct = bartle_quotient.socializer_pct

    return profile

def get_all_profiles():
    return Profile.query.all()

def find_link_minded_players(data):
  
  my_profile = get_profile_by_id(data)
  player_type = get_player_type(my_profile)
  profiles = []

  try:
    if player_type is None:
        raise Exception('This user has not take the bartle test')
      
    key = player_type.get("key")
    value = player_type.get("value")

    if key == 'A':
        profiles =  db.session.query.fliter_by(Profile, BartleQuotient).join(Profile, BartleQuotient.profile_id == Profile.id, isouter=True).filter(BartleQuotient.achiever_pct >= value).all()
    if key == 'E':
        profiles =  db.session.query.filter_by(Profile, BartleQuotient).join(Profile, BartleQuotient.profile_id == Profile.id, isouter=True).filter(BartleQuotient.explorer_pct >= value).all()
    if key == 'K':
        profiles =  db.session.query.filter_by(Profile, BartleQuotient).join(Profile, BartleQuotient.profile_id == Profile.id, isouter=True).filter(BartleQuotient.killer_pct >= value).all()
    if key == 'S':
        profiles =  db.session.query.filter_by(Profile, BartleQuotient).join(Profile, BartleQuotient.profile_id == Profile.id, isouter=True).filter(BartleQuotient.socializer_pct >= value).all()
    
    my_friends = get_my_friends(data)
    if my_friends is not None:
        profile_results = []
        for p in profiles:
            temp = my_friends.query.filter_by(id == p.id).first()
            if temp is None:
                profile_results.append(temp)
    else:
        return profiles

    return profiles
  except Exception as e:
        response_object = {
        'status': 'fail',
        'message': str(e)
        }

        return response_object

def get_player_type(profile):
   df = { 
       'A': profile.achiever_pct, 
       'E': profile.explorer_pct,
       'K' : profile.killer_pct,
       'S' : profile.socializer_pct
    }
   
   key = max(df)
   value = max(df.values())
   result =  {key: value}
   return result
 
def get_my_friends(accountid):
    # creating list

    profiles = []
    profilefriendships = Profile.query.filter_by(account_id=accountid).join(ProfileFriendship, Profile.id == ProfileFriendship.profile_id).all()
    for profilefriendship in profilefriendships:
        for friend in profilefriendship.friends:
           profile = Profile.query.filter_by(id = friend.friends_profile_id).first()     
           profiles.append(profile)

    return profiles

def send_invitation(data):
    myprofile = Profile.query.filter_by(account_id=data['current_account_id']).first()
    myfriendsprofile = Profile.query.filter_by(account_id=data['friend_account_id']).first()

    friendshipcount=False
    profile_lookup = Friends.query.filter_by(friends_profile_id=myfriendsprofile.id).first()
    if profile_lookup is not None:
        friendshipcount = ProfileFriendship.query.filter_by(profile_id=myprofile.id, friend_id=profile_lookup.id).count()
    
    #add check to see if invitiation already exists
    invitationcount = FriendshipInvitations.query(account_id=myprofile.account_id, account_id_to=myfriendsprofile.account_id).count()
 
    try:
        if myprofile is None:
            raise Exception('Current profile is not found')
        if myprofile.account_id==data['friend_account_id']:
            raise Exception('You cannot friend yourself')
        if myfriendsprofile is None:
            raise Exception('Friend''s account is not found')
        if friendshipcount > 0:
            raise Exception('{} is already a friend'.format(myfriendsprofile.friendly_name))
        if invitationcount == 1:
            raise Exception('Invitation already sent to {}').format(myfriendsprofile.friendly_name)
        
        new_invitation = FriendshipInvitations(account_id = myprofile.account_id, raccoiunt_id_to=myfriendsprofile.id)
        save_changes(new_invitation)

        response_object = {
            'status': 'success',
            'message': 'Your invitation was sent to {}}'.format(myfriendsprofile.friendly_name)
        }
    except Exception as e:
         response_object = {
            'status': 'fail',
            'message': str(e)
        }

    return response_object, 
    
def add_a_friend(data):
    myprofile = Profile.query.filter_by(account_id=data['current_account_id']).first()
    myfriendsprofile = Profile.query.filter_by(account_id=data['friend_account_id']).first()

    #Replace in Sprint 3
    count = 0
    profile_lookup = Friends.query.filter_by(friends_profile_id=myfriendsprofile.id).first()
    if profile_lookup is not None:
        count = ProfileFriendship.query.filter_by(profile_id=myprofile.id, friend_id=profile_lookup.id).count()
  
    try:
        if myprofile is None:
            raise Exception('Current profile is not found')
        if myprofile.account_id==data['friend_account_id']:
            raise Exception('You cannot friend yourself')
        if myfriendsprofile is None:
            raise Exception('Friend''s account is not found')
        if count > 0:
            raise Exception('{} is already a friend'.format(myfriendsprofile.friendly_name))
        
        new_friend = Friends(name=myfriendsprofile.friendly_name, friends_profile_id=myfriendsprofile.id)
        db.session.add(new_friend)

        myprofile.friends.append(new_friend)
    
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'You are friends with {}'.format(myfriendsprofile.friendly_name)
        }
    except Exception as e:
         response_object = {
            'status': 'fail',
            'message': str(e)
        }

    return response_object,

def remove_a_friend(data):
    myprofile = Profile.query.filter_by(account_id=data['current_account_id']).first()
    myfriendsprofile = Profile.query.filter_by(account_id=data['friend_account_id']).first()
      
    myfriend, profilefriendship = db.session.query(Friends, ProfileFriendship).join(Friends, ProfileFriendship.friend_id == Friends.id, isouter=True).filter(Friends.friends_profile_id==myfriendsprofile.id and ProfileFriendship.profile_id==myprofile.id).first()
  
    try:
        if myprofile is None:
            raise Exception('Current profile is not found')
        if myprofile.account_id==data['friend_account_id']:
            raise Exception('You cannot unfriend yourself')
        if myfriendsprofile is None:
            raise Exception('Friend''s account is not found')
        if myfriend is None and profilefriendship is None:
            raise Exception('{} is not your friend'.format(myfriendsprofile.friendly_name))      
       
        myprofile.friends.remove(myfriend)
        db.session.commit()
        response_object = {
            'status': 'success',
            'message': 'You are no longer friends with {}'.format(myfriendsprofile.friendly_name)
        }

    except Exception as e:
         response_object = {
            'status': 'fail',
            'message': str(e)
        }

    return response_object, 

def save_changes(data):
    try:
        db.session.add(data)
        db.session.commit()
    except:
        db.session.rollback()
