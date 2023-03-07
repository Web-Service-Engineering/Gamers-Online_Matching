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

class AccountDto:
    api = Namespace('account', description='account related operations')
    account = api.model('account', {
        'email': fields.String(required=True, description='user email address'),
        'password': fields.String(required=True, description='user password'),
        'id': fields.String(description='user Identifier')
    })

class ProfileDto:
    api = Namespace('profile', description='profile related operations')
    profile = api.model('profile', {
        'account_id': fields.Integer(required=True, description='account id - primary key'),
        'first_name': fields.String(required=True, description='first name'),
        'last_name': fields.String(required=False, description='last name'),
        'friendly_name': fields.String(required=False, description='friendly name'),
        'city': fields.String(required=False, description='city'),
        'state': fields.String(required=False, description='state'),
        'date_of_birth': fields.String(required=True, description='date of birth'),
        'skillset_id': fields.String(required=True, description='skillset id'),
        'gender': fields.String(required=True, description='gender'),
        'id': fields.String(description='user Identifier')
    })