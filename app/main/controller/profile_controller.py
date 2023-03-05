from flask import request
from flask_restx import Resource

from ..util.dto import ProfileDto
from ..service.account_service import get_all_profiles, get_profile_by_id, save_new_profile

api = ProfileDto.api
_profile = ProfileDto.profile
    
@api.route('/')
class ProfileList(Resource):   
    @api.doc('list_of_profiles')
    @api.marshal_list_with(_profile, envelope='data')
    def get(self):
        """List all profiles"""
        return get_all_profiles()

    @api.response(201, 'Profile successfully created.')
    @api.doc('Create a new profile for a given account')
    @api.expect(_profile, validate=True)
    def post(self):
        """Creates a new profile for a given account """
        data = request.json
        return save_new_profile(data=data)

@api.route('/<account_id>')
@api.param('account_id', 'The Account identifier')
@api.response(404, 'Profile not found.')
class Profile(Resource):
    @api.doc('get profile by account id')
    @api.marshal_with(_profile)
    def get(self, account_id):
        """get a profile given its account identifier"""
        profile = get_profile_by_id(account_id)
        if not profile:
            api.abort(404)
        else:
            return profile
        
        
