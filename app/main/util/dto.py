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