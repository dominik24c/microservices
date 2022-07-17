from marshmallow import Schema, fields, validate

class GamesListSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    avg_rating = fields.Integer(required=True, validate=validate.Range(min=1, max=5))

class GameSchema(Schema):
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    review = fields.Str(required=True, validate=validate.Length(min=1, max=1000))
    rating = fields.Integer(required=True, validate=validate.Range(min=1, max=5))
    categories = fields.List(fields.Str(validate=validate.Length(min=1, max=60)))