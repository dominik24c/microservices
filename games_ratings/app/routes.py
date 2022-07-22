from flask import (
    Blueprint, Response
)

from .db import mongo
from .schemas import GameRatingSchema

bp = Blueprint('games_ratings', __name__, url_prefix='/games-ratings')

@bp.get('/')
def games_ratings_list() -> Response:
    data = mongo.db.game_ratings.aggregate([ 
        {"$addFields": {"rating": {"$round": [{"$divide":["$total_ratings", "$count_ratings"]}, 2]}}},
        {"$project" : {'_id': 0, 'name': 1, 'rating': 1, 'count_ratings': 1}}
    ])
    schema = GameRatingSchema(many=True)
    return {"games": schema.dump(data)}, 200