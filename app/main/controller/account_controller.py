from flask import request
from flask_restx import Resource

from ..util.dto import AccountDto
from ..service.account_service import save_new_account, get_all_accounts, get_account_by_id, get_account_by_email

api = AccountDto.api
_account = AccountDto.account

@api.route('/')
class AccountList(Resource):
    @api.doc('list_of_registered_accounts')
    @api.marshal_list_with(_account, envelope='data')
    def get(self):
        """List all registered accounts"""
        return get_all_accounts()

    @api.response(201, 'Account successfully created.')
    @api.doc('Create a new account')
    @api.expect(_account, validate=True)
    def post(self):
        """Creates a new User """
        data = request.json
        return save_new_account(data=data)     

@api.route('/<account_id>')
@api.param('account_id', 'The Account identifier')
@api.response(404, 'Account not found.')
class Account(Resource):
    @api.doc('get an account')
    @api.marshal_with(_account)
    def get(self, account_id):
        """get a account given its identifier"""
        account = get_account_by_id(account_id)
        if not account:
            api.abort(404)
        else:
            return account

@api.route('/<email>')
@api.param('email', 'The Email identifier')
@api.response(404, 'Account not found.')
class Account(Resource):
    @api.doc('get an account by email')
    @api.marshal_with(_account)
    def get(self, email):
        """get a account by email"""
        account = get_account_by_email(email)
        if not account:
            api.abort(404)
        else:
            return account

