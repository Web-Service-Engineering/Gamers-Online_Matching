# app/__init__.py

from flask_restx import Api
from flask import Blueprint

#from .main.controller.user_controller import api as user_ns
from .main.controller.account_controller import api as account_ns
from .main.controller.profile_controller import api as profile_ns
from .main.controller.authenticate_controller import api as authenticate_ns
from .main.controller.bartlequotient_controller import api as bartlequotient_ns

blueprint = Blueprint('api', __name__)

api = Api(blueprint,
          title='FLASK RESTPLUS API BOILER-PLATE WITH JWT',
          version='1.0',
          description='a boilerplate for flask restplus web service'
          )

#api.add_namespace(user_ns, path='/user')
api.add_namespace(account_ns, path='/account')
api.add_namespace(profile_ns, path='/profile')
api.add_namespace(bartlequotient_ns, path='/bartlequotient')
api.add_namespace(authenticate_ns, path='/authenticate')