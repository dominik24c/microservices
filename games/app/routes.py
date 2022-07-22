import requests
from bson import ObjectId
from flask import (
    Blueprint, Response,
    request
)
from webargs.flaskparser import use_args

from .schemas import (
    GameSchema, GamesListSchema
)
from .db import mongo
from .producer import mb

bp = Blueprint('games', __name__, url_prefix='/games')


@bp.post('/')
@use_args(GameSchema(), location='json')
def create_game(game_data) -> Response:
    response = requests.get('http://auth:7001/auth/verify', headers=request.headers)
    data = response.json()

    if response.status_code == 200:
        id = data.get('user_id')
        game_name = game_data['name']

        game = mongo.db.users.find_one({'_id': ObjectId(id), 'games.name': game_name})
        if game:
            return {"message": "You have just rated this game!"}, 400

        if 'categories' not in game_data.keys():
            game_data['categories'] = []
        result = mongo.db.users.update_one({"_id": ObjectId(id)}, {'$push':{'games': game_data}})

        if result.modified_count > 0:
            mb.pubish('create_game_ratings', {'name': game_data['name'], 'rating': game_data['rating']})
            return {"message": f"Game was created!"}, 201
        else:
            return {"message": "Something went wrong!"}, 400
    return data, response.status_code

@bp.get('/')
def list_games() -> Response:
    games = mongo.db.users.aggregate([
        {"$project": {"_id": 0, "games": 1}},
        {"$unwind": "$games"},
        {"$group":{"_id": "$games.name", "avg_rating": {"$avg": "$games.rating"}}},
        {"$project": {"name":"$_id", "avg_rating": 1,"_id": 0}},
        {"$sort": {"avg_rating": -1}}
    ])
    schema = GamesListSchema(many=True)
    return {"games": schema.dump(games)}, 200

@bp.get('/<game_name>/')
def retrieve_game(game_name: str) -> Response:
    response = requests.get('http://auth:7001/auth/verify', headers=request.headers)
    data = response.json()

    if response.status_code == 200:
        id = data.get('user_id')
        games = mongo.db.users.aggregate([
            {"$project":{"_id": 1, "games.name": 1, 'games.review': 1, 'games.rating': 1, "games.categories": 1}},
            {"$unwind": "$games"},
            {"$match": {"_id": ObjectId(id), "games.name": game_name}},
            {"$project": {"_id":0}},
        ])

        game_result = list(games)

        if len(game_result) > 0:
            schema = GameSchema()
            game = game_result[0]['games']
            return schema.dump(game), 200

        return {"message": "Not found game!"}, 404

    return data, response.status_code

@bp.delete('/<game_name>/')
def delete_game(game_name: str) -> Response:
    response = requests.get('http://auth:7001/auth/verify', headers=request.headers)
    data = response.json()

    if response.status_code == 200:
        id = data.get('user_id')
        
        user = mongo.db.users.find_one({"_id": ObjectId(id), 'games.name': game_name})

        result = mongo.db.users.update_one(
            {"_id": ObjectId(id)},
            {"$pull": {"games": {"name": game_name}}}
        )

        if user and result.modified_count > 0:
            game = user['games'][0]
            mb.pubish('delete_game_ratings', {'name': game['name'], 'rating': game['rating']})
            return {}, 204

        return {"message": "Not found game!"}, 404

    return data, response.status_code
