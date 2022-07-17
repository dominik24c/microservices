from marshmallow import Schema, fields

class UserSchema(Schema):
    username=fields.Str(required=True)
    first_name=fields.Str(required=True)
    last_name= fields.Str(required=True)

class UserCreateSchema(UserSchema):
    password=fields.Str(required=True)
    email=fields.Email(required=True)

class UserLoginSchema(Schema):
    username=fields.Str(required=True)
    password=fields.Str(required=True)
