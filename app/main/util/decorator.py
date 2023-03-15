from functools import wraps

from flask import request

from app.main.service.account_service import Auth
from typing import Callable


def token_required(f) -> Callable:
    @wraps(f)
    def decorated(*args, **kwargs):

        data, status = Auth.get_logged_in_account(request)
        token = data.get('data')

        if not token:
            return data, status

        return f(*args, **kwargs)

    return decorated