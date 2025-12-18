"""
Django settings for backend project.

基于本地SQLite构建，配合ER文档定义的实体。注意：需在运行环境安装
Django (>=4.2)。当前仓库因无网络未自动安装，请在可联网环境执行
`pip install "Django>=4.2,<5"`。
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "dev-secret-key-change-me"

DEBUG = True

ALLOWED_HOSTS: list[str] = []

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "core.middleware.SimpleCorsMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "backend.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "backend.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
        "OPTIONS": {
            "timeout": 10,
        },
    }
}

AUTH_PASSWORD_VALIDATORS: list = []

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "static/"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Session 配置
SESSION_COOKIE_NAME = "sessionid"
SESSION_COOKIE_AGE = 86400 * 7  # 7天
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"  # 对于同站请求，Lax 可以工作
SESSION_SAVE_EVERY_REQUEST = False
SESSION_COOKIE_SECURE = False  # 开发环境设为 False（localhost），生产环境应设为 True（需要 HTTPS）
# 注意：localhost:5173 到 127.0.0.1:8000 被视为跨域，但 SameSite=Lax 在大多数浏览器中可以工作

