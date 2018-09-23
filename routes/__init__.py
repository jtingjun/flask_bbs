import uuid
from flask import session, request, abort
from functools import wraps
from models.user import User


def current_user():
    uid = session.get('user_id', -1)
    if uid != -1:
        u = User.one(id=uid)
    else:
        u = User.one(role_id=1)
    return u


csrf_tokens = dict()


def csrf_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.args['token']
        u = current_user()
        if token in csrf_tokens and csrf_tokens[token] == u.id:
            csrf_tokens.pop(token)
            return f(*args, **kwargs)
        else:
            abort(401)

    return wrapper


def new_csrf_token():
    u = current_user()
    token = str(uuid.uuid4())
    csrf_tokens[token] = u.id
    return token
