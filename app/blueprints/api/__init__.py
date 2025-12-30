from flask import Blueprint


api = Blueprint(
    name = "api",
    import_name = __name__,
    url_prefix = "/api"
)

from app.blueprints.api import routes