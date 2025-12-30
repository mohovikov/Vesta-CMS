from typing import Any
from flask import Response, json


def json_response(data: Any, status: int = 200) -> Response:
    """
    Возвращает JSON ответ с поддержкой кириллицы без экранирования.
    
    :param data: любой сериализуемый объект (dict, list и т.д.)
    :param status: HTTP статус код
    :return: flask.Response
    """
    return Response(
        json.dumps(data, ensure_ascii = False, indent = None),
        status = status,
        mimetype = "application/json"
    )