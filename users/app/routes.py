import requests
from flask import (
    Blueprint, Response,
    request
    # jsonify, make_response,
    # request
)
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)
from webargs.flaskparser import use_args

from .schemas import (
    UserSchema, UserCreateSchema,
    UserLoginSchema
)
from .db import mongo

bp = Blueprint('users', __name__, url_prefix='/users')


@bp.post('/register')
@use_args(UserCreateSchema(), location='json')
def register(user)->Response:
    print(user)
    password = user.get('password')
    password = generate_password_hash(password)
    u = mongo.db.users.insert_one({**user, 'password': password})
    return {"message": f"User was created {u.inserted_id}!"}, 201

@bp.get('/')
def show_users() -> Response:
    users = mongo.db.users.find({}, {'_id':0, 'first_name': 1, 'last_name':1, 'username': 1})
    schema = UserSchema(many=True)
    return {"users": schema.dump(users)}, 200

@bp.post('/login')
@use_args(UserLoginSchema(), location='json')
def login(user) -> Response:
    username = user.get('username')
    u = mongo.db.users.find_one({'username': username},{'_id':1, 'password':1})
    print
    if u is None:
        return {"message": "User doesn't exist!"}, 400
    if not check_password_hash(u.get('password'), user.get('password')):
        return {"message": "Invalid password!"}, 400

    id = str(u.get('_id'))
    # print(username ,id)
    # token = authorize(id, username)
    # print(token)

    response = requests.post('http://auth:7001/auth/token', json={'id': id, 'username': username})
    # print(response.bo)
    if response.status_code == 201:
        return response.json(), 200
    
    return response.json(), response.status_code

@bp.get('/restrict')
def restrict_view() -> Response:
    response = requests.get('http://auth:7001/auth/verify', headers=request.headers)
    print(response.status_code)
    if response.status_code == 204:
        return {"view": "ok"}, 200
    return response.json(), response.status_code