from flask import Blueprint


site = Blueprint(
    name = "site",
    import_name = __name__,
    url_prefix = "/"
)

from app.blueprints.site import routes