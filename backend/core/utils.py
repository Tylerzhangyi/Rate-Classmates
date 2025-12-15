import json
from typing import Any, Callable

from django.http import HttpRequest, JsonResponse


def parse_json(request: HttpRequest) -> dict[str, Any]:
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return {}


def api_response(code: int = 200, message: str = "success", data: Any | None = None, status: int | None = None) -> JsonResponse:
    return JsonResponse({"code": code, "message": message, "data": data}, status=status or code, safe=False)


def allow_methods(methods: list[str]) -> Callable:
    def decorator(func: Callable) -> Callable:
        def wrapper(request: HttpRequest, *args, **kwargs):
            if request.method not in methods:
                return api_response(405, "method not allowed", status=405)
            return func(request, *args, **kwargs)

        return wrapper

    return decorator

