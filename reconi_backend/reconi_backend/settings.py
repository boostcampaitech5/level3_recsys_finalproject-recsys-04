"""
Django settings for reconi_backend project.

Generated by 'django-admin startproject' using Django 4.2.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
import datetime
from pathlib import Path

import environ


def create_file_if_not_exists(file_path):
    # 파일이 존재하는지 확인
    if not os.path.exists(file_path):
        # 파일이 존재하지 않으면 경로와 파일 생성
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as f:
            f.write("")


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))

INFERENCE_COLDSTART = os.getenv("INFERENCE_COLDSTART", "")
INFERENCE_NOTCOLDSTART = os.getenv("INFERENCE_NOTCOLDSTART", "")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY", "")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Swagger
    "drf_yasg",
    # RestFramework
    "rest_framework",
    "rest_framework.authtoken",
    "rest_framework_simplejwt",
    "dj_rest_auth",
    "dj_rest_auth.registration",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    # Apps
    "coffee_bean.apps.CoffeeBeanConfig",
    "user.apps.UserConfig",
    # CORS
    "corsheaders",
]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    # Logging
    "coffee_bean.middleware.LogMiddleware",
]

ROOT_URLCONF = "reconi_backend.urls"

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

WSGI_APPLICATION = "reconi_backend.wsgi.application"

AUTH_USER_MODEL = "user.ReconiUser"

JWT_AUTH_COOKIE = "my-app-auth"
JWT_AUTH_REFRESH_COOKIE = "my-refresh-token"

SITE_ID = 1
REST_USE_JWT = True

ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_LOGOUT_ON_GET = True
LOGOUT_ON_PASSWORD_CHANGE = True

ACCOUNT_FORMS = {"signup": "user.forms.MyCustomSignupForm"}


REST_AUTH = {
    "JWT_AUTH_COOKIE": "my-app-auth",
    "JWT_AUTH_REFRESH_COOKIE": "my-refresh-token",
    "REGISTER_SERIALIZER": "user.serializers.ReconiRegisterSerializer",
    "REGISTER_PERMISSION_CLASSES": ("rest_framework.permissions.AllowAny",),
    "ACCOUNT_UNIQUE_EMAIL": True,
    "USE_JWT": True,
    "ACCOUNT_USER_MODEL_USERNAME_FIELD": None,
    "ACCOUNT_USERNAME_REQUIRED": False,
    "ACCOUNT_EMAIL_REQUIRED": True,
    "ACCOUNT_AUTHENTICATION_METHOD": "email",
    "ACCOUNT_EMAIL_VERIFICATION": "none",
    "ACCOUNT_LOGOUT_ON_GET": True,
    "LOGOUT_ON_PASSWORD_CHANGE": True,
    "JWT_AUTH_COOKIE_USE_CSR": True,
    # "ACCOUNT_ADAPTER": "user.adapters.CustomAccountAdapter",
}

SIMPLE_JWT = {
    "USER_ID_FIELD": "email",
    "ACCESS_TOKEN_LIFETIME": datetime.timedelta(hours=2),
    "REFRESH_TOKEN_LIFETIME": datetime.timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": False,
    "BLACKLIST_AFTER_ROTATION": True,
}

ACCOUNT_ADAPTER = "user.adapters.CustomAccountAdapter"

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticatedOrReadOnly",  # or allow read-only access for unauthenticated users.
        # "rest_framework.permissions.IsAuthenticated",  # 인증된 사용자만 접근 가능
        # 'rest_framework.permissions.IsAdminUser', # 관리자만 접근 가능
    ),
    "DEFAULT_RENDERER_CLASSES": (
        # 자동으로 json으로 바꿔줌
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": [
        # "rest_framework.authentication.SessionAuthentication",  # 세션 인증을 사용하는 경우
        # "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
        "dj_rest_auth.jwt_auth.JWTCookieAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}

# CORS 권한
CORS_ALLOW_ALL_ORIGINS = True  # <- 모든 호스트 허용

# or
# CORS_ALLOWED_ORIGINS = [
# "http://localhost:3000",
# "http://127.0.0.1:3000"
# ]

# CORS_ALLOW_CREDENTIALS가 True인 경우, 쿠키가 cross-site HTTP 요청에 포함될 수 있다. 기본값은 False이다.
CORS_ALLOW_CREDENTIALS = True


# 실제 요청에 허용되는 HTTP 동사 리스트이다. 기본값은 다음과 같다:

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# 실제 요청을 할 때 사용될 수 있는 non-standard HTTP 헤더 목록이다. 기본값을 다음과 같다:

CORS_ALLOW_HEADERS = [
    "accept",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
]

## JWT Authenticated
# REST_FRAMEWORK = {
#     'DEFAULT_PERMISSION_CLASSES': (
#         'rest_framework.permissions.IsAuthenticated',
#         'rest_framework.permissions.IsAdminUser',
#         'rest_framework.permissions.AllowAny',
#     ),
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
#     ),
#     'DEFAULT_FILTER_BACKENDS': [
#             'django_filters.rest_framework.DjangoFilterBackend'
#     ],
# }

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("DB_NAME", "appseed_db"),
        "USER": os.getenv("DB_USERNAME", "appseed_db_usr"),
        "PASSWORD": os.getenv("DB_PASS", "pass"),
        "HOST": os.getenv("DB_HOST", "localhost"),
        "PORT": os.getenv("DB_PORT", "3306"),
    },
}

create_file_if_not_exists(os.path.join(BASE_DIR, "logs", "user_logs.log"))

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "user_logs": {
            "level": "DEBUG",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(BASE_DIR, "logs", "user_logs.log"),
            "maxBytes": 1024 * 1024 * 1024,  # 파일 크기 제한 (1024MB)
            "backupCount": 5,  # 보관할 백업 파일 수
            "formatter": "verbose",  # 로그 포맷 설정
        },
    },
    "formatters": {
        "verbose": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        },
    },
    "loggers": {
        "user_logs": {
            "handlers": ["user_logs"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     # "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    # },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    # {
    #     # "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    # },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "static/"
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")
# STATICFILES_DIRS = [
#     # os.path.join(BASE_DIR, "coffee_bean", "static"),
#     # os.path.join(BASE_DIR, "user", "static"),
# ]
# STATIC_ROOT = os.path.join(BASE_DIR, "static")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
