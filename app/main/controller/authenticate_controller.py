from flask import request
from flask_restx import Resource

from ..util.dto import AuthAccountDto
from ..service.account_service import login_user, logout_user, get_logged_in_account

api = AuthAccountDto.api
_account = AuthAccountDto.auth_account


@api.route('/login')
class Login(Resource):

    @api.doc('Login in user')
    @api.expect(_account, validate=True)
    def post(self):
        """ login in user """
        data = request.json
        return login_user(data=data)

#Write logout method
@api.route('/logout')
class Logout(Resource):
    @api.doc('Logout user')
    def post(self):
        """ logout user """
        # get auth token
        auth_header = request.headers.get('Authorization')    
        return logout_user(data=auth_header) 
    
#Write logout method
@api.route('/getloggedinaccount')
class GetLoggedInAccount(Resource):
    @api.doc('Get logged in account')
    def post(self):
        """ logout in account  """
        # get auth token
        auth_header = request.headers.get('Authorization')
    
        return get_logged_in_account(data=auth_header) 
