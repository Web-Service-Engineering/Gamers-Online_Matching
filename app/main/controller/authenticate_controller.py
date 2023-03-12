from flask import request
from flask_restx import Resource

from ..util.dto import AuthAccountDto
from ..service.account_service import login_user, logout_user

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

    # Write logout method
    @api.route('/logout')
    class Login(Resource):
        @api.doc('Logout in user')
        #@api.expect(_account, validate=True)
        def post(self):
            """ logout user """
            data = request.json
            return logout_user(data=data)
