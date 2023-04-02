#Data transfer object (DTO) responsible for carrying data between proesses.  In this case
#will be used to marshal data for our API calls.

from flask_restx import Namespace, fields


class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'name': fields.String(required=True, description='user username'),
        #'password': fields.String(required=True, description='user password'),
         'id': fields.String(description='user Identifier')
    })

class AuthAccountDto:
    api = Namespace('auth', description='authentication related operations')
    auth_account = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The account password '),
    })

class AccountDto:
    api = Namespace('account', description='account related operations')
    account = api.model('account', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'id': fields.String(description='account Identifier')
    })

class ProfileDto:
    api = Namespace('profile', description='profile related operations')
    profile = api.model('profile', {
        'account_id': fields.String(required=True, description='account id'),
        'first_name': fields.String(required=True, description='first name'),
        'last_name': fields.String(required=False, description='last name'),
        'friendly_name': fields.String(required=False, description='friendly name'),
        'city': fields.String(required=False, description='city'),
        'state': fields.String(required=False, description='state'),
        'date_of_birth': fields.String(required=True, description='date of birth'),
        'skillset_id': fields.String(required=True, description='skillset id'),
        'gender': fields.String(required=True, description='gender'),
        'achiever_pct': fields.String(required=False, description='achiever_pct'),
        'explorer_pct': fields.String(required=False, description='explorer_pct'),
        'killer_pct': fields.String(required=False, description='killer_pct'),
        'socializer_pct': fields.String(required=False, description='socializer_pct'),
        'id': fields.String(description='profile Identifier')
    })


class BartleQuotientDto:
    api = Namespace('bartlequotient', description='bartle test related operations')
    bartlequotient = api.model('bartlequotient', {
        'account_id': fields.String(required=True, description='account_id'),
        'responses': fields.List(fields.String(),  required=True,  description='list of bartle test responses')
    })

class ProfileFriendShipDto:
    api = Namespace('profilefriendship', description='friend related operations')
    profilefriendship = api.model('profilefriendship', {
        'current_account_id': fields.Integer(required=True, description='current account id'),
        'friend_account_id': fields.Integer(required=True, description='friend account id')
    })  
 