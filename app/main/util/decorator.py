from functools import wraps

from flask import request

from app.main.service.auth_service import get_logged_in_account
from typing import Callable


def token_required(f) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'X-API-KEY' in request.headers:
            token = request.headers.get('X-API-KEY')

        if not token:
            return {'message' : 'Token is missing'}, 401
       
        data, status = get_logged_in_account(token)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated