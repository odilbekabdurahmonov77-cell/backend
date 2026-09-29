"""
Django settings for IQ Test Platform.
Works locally (SQLite) and on Railway / Render (PostgreSQL) automatically.
"""
from pathlib import Path
from datetime import timedelta
import os

import dj_database_url
from decouple import config

# ──────────────────────── Paths ────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent

# ──────────────────────── Security ────────────────────────
SECRET_KEY = config("DJANGO_SECRET_KEY", default="dev-insecure-change-me")
DEBUG = config("DEBUG", default=True, cast=bool)

# ──────────────────────── Allowed Hosts ────────────────────────
# Default: lokal + Railway + Render subdomenlari
ALLOWED_HOSTS = [
    h.strip()
    for h in config(
        "DJANGO_ALLOWED_HOSTS",
        default="localhost,127.0.0.1,.up.railway.app,.onrender.com",
    ).split(",")
    if h.strip()
]

# Railway'da RAILWAY_PUBLIC_DOMAIN avtomatik qo'shiladi
if not DEBUG:
    railway_domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")
    if railway_domain and railway_domain not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(railway_domain)

    render_domain = os.environ.get("RENDER_EXTERNAL_HOSTNAME")
    if render_domain and render_domain not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(render_domain)

# ──────────────────────── Applications ────────────────────────
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",

    "apps.accounts",
    "apps.testing",
]

# ──────────────────────── Middleware ────────────────────────
MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ──────────────────────── Templates ────────────────────────
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
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

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# ──────────────────────── Database ────────────────────────
DATABASES = {
    "default": dj_database_url.config(
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ──────────────────────── Password validation ────────────────────────
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ──────────────────────── i18n ────────────────────────
LANGUAGE_CODE = "en"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ──────────────────────── Static files ────────────────────────
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

# Faqat mavjud bo'lsa qo'shamiz (Render/Railway'da static/ yo'q)
STATICFILES_DIRS = []
STATIC_DIR = BASE_DIR / "static"
if STATIC_DIR.exists():
    STATICFILES_DIRS.append(STATIC_DIR)

# Whitenoise manifest — debug rejimida oddiy storage
if DEBUG:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage",
        },
    }
else:
    STORAGES = {
        "default": {
            "BACKEND": "django.core.files.storage.FileSystemStorage",
        },
        "staticfiles": {
            "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
        },
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ──────────────────────── DRF ────────────────────────
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.AllowAny",       # Test anonim ishlashi uchun
    ),
    "DEFAULT_RENDERER_CLASSES": ("rest_framework.renderers.JSONRenderer",),
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
}

# ──────────────────────── CORS ────────────────────────
# Origin'larni olish + slash va bo'sh joyni avtomatik tozalash
CORS_ALLOWED_ORIGINS = []
_raw_cors = config(
    "CORS_ALLOWED_ORIGINS",
    default=(
        "http://localhost:5173,"
        "http://127.0.0.1:5173,"
        "https://iq-test-frontend.onrender.com,"
        "https://iq-test-frontend-production-c134.up.railway.app"
    ),
)
for origin in _raw_cors.split(","):
    origin = origin.strip().rstrip("/")   # ← slash va bo'sh joyni olib tashlash
    if origin:
        CORS_ALLOWED_ORIGINS.append(origin)

# ──────────────────────── CSRF ────────────────────────
CSRF_TRUSTED_ORIGINS = []
_raw_csrf = config(
    "CSRF_TRUSTED_ORIGINS",
    default=(
        "http://localhost:5173,"
        "https://iq-test-frontend.onrender.com,"
        "https://backendiqtest.onrender.com,"
        "https://backend-production-e4320.up.railway.app,"
        "https://iq-test-frontend-production-c134.up.railway.app"
    ),
)
for origin in _raw_csrf.split(","):
    origin = origin.strip().rstrip("/")
    if origin:
        CSRF_TRUSTED_ORIGINS.append(origin)

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-language",
    "content-type",
    "authorization",
    "x-csrftoken",
    "x-requested-with",
]

CORS_ALLOW_CREDENTIALS = True

# ──────────────────────── Security (prod only) ────────────────────────
if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
    SECURE_SSL_REDIRECT = False             # Railway allaqachon HTTPS
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# ──────────────────────── Payment ────────────────────────
ADMIN_PAYMENT_ACCOUNT = config("ADMIN_PAYMENT_ACCOUNT", default="")
ADMIN_PAYMENT_HOLDER = config("ADMIN_PAYMENT_HOLDER", default="CogniTest")