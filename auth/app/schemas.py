from marshmallow import Schema, fields

class TokenSchema(Schema):
    id=fields.Str(required=True)
    username=fields.Str(required=True)
