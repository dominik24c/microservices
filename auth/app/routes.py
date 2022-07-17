import jwt
from bson import ObjectId
from flask import Blueprint, Response
from webargs.flaskparser import use_args

from .db import mongo
from .auth import get_token, verify_token
from .schemas import TokenSchema

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.post('/token')
@use_args(TokenSchema(), location='json')
def get_token_view(token_data)->Response:
    token = get_token(**token_data)
    return {"token": token}, 201

@bp.get('/verify')
def verify_token_view()-> Response():
    try:
        payload = verify_token()
    except jwt.ExpiredSignatureError:
        return {"message": "Your signature has expired!"}, 401

    mongo.db.users.find_one_or_404({"_id": ObjectId(payload.get('id'))})
    return {}, 204