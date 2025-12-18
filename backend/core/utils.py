import json
from functools import wraps
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


def require_auth(view_func: Callable) -> Callable:
    """
    认证装饰器：检查用户是否已登录（通过 session）
    """
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if 'user_id' not in request.session:
            return api_response(401, "未登录，请先登录", status=401)
        return view_func(request, *args, **kwargs)

    return wrapper


def require_admin(view_func: Callable) -> Callable:
    """
    管理员认证装饰器：检查用户是否已登录且是管理员
    """
    @wraps(view_func)
    def wrapper(request: HttpRequest, *args, **kwargs):
        if 'user_id' not in request.session:
            return api_response(401, "未登录，请先登录", status=401)
        if request.session.get('role') != 'admin':
            return api_response(403, "需要管理员权限", status=403)
        return view_func(request, *args, **kwargs)

    return wrapper

