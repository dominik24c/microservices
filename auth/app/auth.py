import jwt
from flask import request, current_app, abort


def verify_token():
    """verify auth token"""
    if "Authorization" in request.headers:
        "Bearer secret_token"
        token= request.headers['Authorization'].split()[1]
    else:
        abort(401, "Auth token is missing!")

    decoded = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms='HS256')
    print(decoded)
    return decoded # return dict {id, username}

def get_token(id: str, username: str) -> str:
    """Generate auth token"""
    encoded = jwt.encode({"id": id, "username": username}, current_app.config['SECRET_KEY'], algorithm='HS256')
    return encoded