from app import services
from app.helpers.response import json_response
from app.blueprints.api import api


@api.get("/status")
def api_status():
    return json_response({
        "success": True,
        "message": "API работает",
        "users_count": services.get_users_count()
    })