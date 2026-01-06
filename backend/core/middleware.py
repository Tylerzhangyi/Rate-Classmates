from typing import Iterable

from django.http import HttpResponse


class SimpleCorsMiddleware:
    """
    轻量 CORS 支持，允许前端访问。
    支持开发环境（localhost）和服务器部署（110.40.153.38）。
    如需更严谨控制可替换为 django-cors-headers。
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # 允许的来源列表
        allowed_origins: Iterable[str] = (
            "http://localhost:8805",
            "http://localhost:5002",
            "http://localhost:5000",
            "http://localhost:5173",
            "http://127.0.0.1:8805",
            "http://127.0.0.1:5002",
            "http://127.0.0.1:5000",
            "http://127.0.0.1:5173",
            "http://110.40.153.38",
            "http://110.40.153.38:8805",
            "http://110.40.153.38:5002",
            "http://110.40.153.38:5000",
            "http://110.40.153.38:5173",
            "http://tyler.yunguhs.com",
            "https://tyler.yunguhs.com",
            "http://tyler.yunguhs.com:8805",
        )
        
        # 预检请求直接返回
        if request.method == "OPTIONS":
            response = HttpResponse()
            origin = request.headers.get("Origin")
            if origin in allowed_origins:
                response["Access-Control-Allow-Origin"] = origin
                response["Access-Control-Allow-Credentials"] = "true"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
            return response
        else:
            response = self.get_response(request)

        origin = request.headers.get("Origin")
        if origin in allowed_origins:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Credentials"] = "true"
        response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
        response["Access-Control-Allow-Methods"] = "GET, POST, PUT, PATCH, DELETE, OPTIONS"
        return response

