from marshmallow.schema import Schema
from marshmallow import fields

class GameRatingSchema(Schema):
    name = fields.String(required=True)
    rating = fields.String(required=True)
    count_ratings = fields.String(required=True)