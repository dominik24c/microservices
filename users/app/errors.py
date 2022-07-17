from flask import json, Flask
from werkzeug.exceptions import HTTPException

def register_errors(app: Flask) -> None:
    @app.errorhandler(HTTPException)
    def handle_exception(e):
        response = e.get_response()
        response.data = json.dumps({
            # "code": e.code,
            "name": e.name,
            "description": e.description,
        })
        response.content_type = "application/json"

        return response
