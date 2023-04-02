from flask import request
from flask_restx import Resource

from ..util.dto import ProfileFriendShipDto
from ..service.profile_service import add_a_friend,remove_a_friend
from ..util.decorator import token_required

api = ProfileFriendShipDto.api

_profilefriendship = ProfileFriendShipDto.profilefriendship
        
@api.route('/')
class Profile(Resource):   
    @api.doc('Add a friend')
    @api.expect(_profilefriendship, validate=True)
    def post(self):
        """Creates a new friend """
        data = request.json
        return add_a_friend(data=data)

    @api.doc('Remove a friend')
    @api.expect(_profilefriendship, validate=True)
    def put(self):
        """Removes a friend  """
        data = request.json
        return remove_a_friend(data=data) 
    
        
        


