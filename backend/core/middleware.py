from typing import Iterable

from django.http import HttpResponse


class SimpleCorsMiddleware:
    """
    轻量 CORS 支持，允许前端 http://localhost:5173 访问。
    如需更严谨控制可替换为 django-cors-headers。
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 预检请求直接返回
        if request.method == "OPTIONS":
            response = HttpResponse()
        else:
            response = self.get_response(request)

        allowed_origins: Iterable[str] = ("http://localhost:5173", "http://127.0.0.1:5173")
        origin = request.headers.get("Origin")
        if origin in allowed_origins:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        return response

