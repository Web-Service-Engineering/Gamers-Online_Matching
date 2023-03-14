from flask import request
from flask_restx import Resource

from ..util.dto import  BartleQuotientDto
from ..service.account_service import save_new_bartle_results

api = BartleQuotientDto.api
_bartlequotient = BartleQuotientDto.bartlequotient

@api.route('/')
class BartleQuotientList(Resource):   
    # @api.doc('list_of_profiles')
    # @api.marshal_list_with(_profile, envelope='data')
    # def get(self):
    #     """List all profiles"""
    #     return get_all_profiles()

    #@api.response(201, 'Profile successfully created.')

    @api.doc('Process bartle test responses')
    @api.expect(_bartlequotient, validate=True)
    def post(self):
        """ Processes bartle test resuts """
        data = request.json
        return save_new_bartle_results(data=data)   
    