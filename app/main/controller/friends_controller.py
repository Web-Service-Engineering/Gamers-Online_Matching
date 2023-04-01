from flask import request
from flask_restx import Resource

from ..util.dto import ProfileFriendShipDto
from ..service.profile_service import add_a_friend
from ..util.decorator import token_required


api = ProfileFriendShipDto.api

_profilefriendship = ProfileFriendShipDto.profilefriendship

# class Profiles(Resource):
#     @api.doc('list_of_friends')
#     @api.marshal_list_with(_account)
    
#     def get(self, account_id):
#         """List all friends"""
#         return get_friends(account_id)
   

@api.route('/friends')
class ProfileList(Resource):   
    # @api.doc('list_of_profiles')
    # @api.marshal_list_with(_profile, envelope='data')
    # def get(self):
    #     """List all profiles"""
    #     return get_all_profiles()

    #@api.response(201, 'Profile successfully created.')

    @api.doc('Add a friend')
    @api.expect(_profilefriendship, validate=True)
    def post(self):
        """Creates a new friend """
        data = request.json
        return add_a_friend(data=data)

    # @api.doc('Update a new profile for a given account')
    # @api.expect(_profile, validate=True)
    # def put(self):
    #     """Update a profile for a given account """
    #     data = request.json
    #     return update_profile(data=data) 
    
        

# @api.route('/friends/<friend_id>')
# @api.param('friend_id', 'The friends account identifier')
# @api.response(404, 'Account not found.')
# class Profiles(Resource):
#     @api.doc('remove a friend')
 
#     @api.marshal_with(_account)
#     #@api.doc(security='apikey')
#     @token_required
#     def put(self,friend_id):
#         """remove a friend"""
#         return unfriend(friend_id)
        


