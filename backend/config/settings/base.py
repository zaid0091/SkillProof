"""Settings shared by every environment.

Environment-specific modules (dev, prod, test) import from here and override
only what differs. Configuration is read from environment variables; defaults
exist solely so a fresh checkout can run locally.
"""

from __future__ import annotations

from datetime import timedelta
from pathlib import Path

import environ

# backend/config/settings/base.py -> backend/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    DJANGO_DEBUG=(bool, False),
    DJANGO_ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
    CORS_ALLOWED_ORIGINS=(list, ["http://localhost:3000"]),
    CSRF_TRUSTED_ORIGINS=(list, ["http://localhost:3000"]),
    DATABASE_CONN_MAX_AGE=(int, 60),
    CELERY_TASK_ALWAYS_EAGER=(bool, False),
    MAX_SUBMISSION_BYTES=(int, 2 * 1024 * 1024),
    ASSESSMENT_WORKER_TIMEOUT_SECONDS=(int, 60),
    EMAIL_VERIFICATION_TOKEN_TTL_HOURS=(int, 72),
    PASSWORD_RESET_TOKEN_TTL_MINUTES=(int, 60),
)
environ.Env.read_env(BASE_DIR / ".env")

# --- Core -------------------------------------------------------------------

SECRET_KEY = env.str("DJANGO_SECRET_KEY", default="insecure-development-key-change-me")
DEBUG = env("DJANGO_DEBUG")
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS")

FRONTEND_URL = env.str("FRONTEND_URL", default="http://localhost:3000")

# --- Applications -----------------------------------------------------------

DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "corsheaders",
    "rest_framework",
    "rest_framework_simplejwt.token_blacklist",
]

# Domain modules mirror docs/tad.md section 5.1. Each owns its models, API, and
# permissions; none may reach into another module's tables directly.
LOCAL_APPS = [
    "apps.accounts",
    "apps.organizations",
    "apps.profiles",
    "apps.skills",
    "apps.assessments",
    "apps.submissions",
    "apps.evaluations",
    "apps.evidence",
    "apps.github_integration",
    "apps.hiring",
    "apps.analytics",
    "apps.notifications",
    "apps.audit",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"
ASGI_APPLICATION = "config.asgi.application"

# --- Database ---------------------------------------------------------------

# PostgreSQL is the platform database. SQLite is the fallback so that checks,
# tests, and a first run work without services; Docker Compose and every
# deployed environment supply a PostgreSQL URL.
DATABASES = {
    "default": env.db_url(
        "DATABASE_URL",
        default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}",
    )
}
DATABASES["default"]["CONN_MAX_AGE"] = env("DATABASE_CONN_MAX_AGE")
DATABASES["default"].setdefault("OPTIONS", {})

# --- Authentication ---------------------------------------------------------

AUTH_USER_MODEL = "accounts.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 10},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.ScryptPasswordHasher",
]

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=15),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "UPDATE_LAST_LOGIN": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    "USER_ID_FIELD": "id",
    "USER_ID_CLAIM": "user_id",
    "SIGNING_KEY": SECRET_KEY,
    "AUTH_TOKEN_CLASSES": ("rest_framework_simplejwt.tokens.AccessToken",),
}

# --- API --------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    # Deny by default: every endpoint must opt in to anonymous access explicitly.
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_PARSER_CLASSES": [
        "rest_framework.parsers.JSONParser",
        "rest_framework.parsers.MultiPartParser",
        "rest_framework.parsers.FormParser",
    ],
    "DEFAULT_PAGINATION_CLASS": "common.pagination.DefaultPagination",
    "PAGE_SIZE": 20,
    "EXCEPTION_HANDLER": "common.exceptions.api_exception_handler",
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
}

CORS_ALLOWED_ORIGINS = env("CORS_ALLOWED_ORIGINS")
CORS_ALLOW_CREDENTIALS = True
CSRF_TRUSTED_ORIGINS = env("CSRF_TRUSTED_ORIGINS")

# --- Celery -----------------------------------------------------------------

REDIS_URL = env.str("REDIS_URL", default="redis://localhost:6379/0")

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL", default=REDIS_URL)
CELERY_RESULT_BACKEND = env.str("CELERY_RESULT_BACKEND", default="redis://localhost:6379/1")
CELERY_TASK_ALWAYS_EAGER = env("CELERY_TASK_ALWAYS_EAGER")
CELERY_TASK_EAGER_PROPAGATES = True
CELERY_TIMEZONE = "UTC"
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_ACKS_LATE = True
CELERY_TASK_REJECT_ON_WORKER_LOST = True
CELERY_TASK_TIME_LIMIT = env.int("ASSESSMENT_WORKER_TIMEOUT_SECONDS", default=60) + 30
CELERY_TASK_SOFT_TIME_LIMIT = env.int("ASSESSMENT_WORKER_TIMEOUT_SECONDS", default=60)
CELERY_WORKER_MAX_TASKS_PER_CHILD = 50
CELERY_RESULT_EXPIRES = 60 * 60  # 1 hour

# --- Caching ----------------------------------------------------------------

# LocMem is the safe local default. Deployments should set REDIS_URL-backed cache.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "skillproof-local",
    }
}

# --- Email ------------------------------------------------------------------

EMAIL_BACKEND = env.str("EMAIL_BACKEND", default="django.core.mail.backends.console.EmailBackend")
DEFAULT_FROM_EMAIL = env.str("DEFAULT_FROM_EMAIL", default="SkillProof <no-reply@skillproof.local>")

# --- Authentication tokens --------------------------------------------------

# Email-verification links stay valid for days; password-reset links are short
# lived. Both token types are single use (docs/sacs.md section 3.5).
EMAIL_VERIFICATION_TOKEN_TTL_HOURS = env("EMAIL_VERIFICATION_TOKEN_TTL_HOURS")
PASSWORD_RESET_TOKEN_TTL_MINUTES = env("PASSWORD_RESET_TOKEN_TTL_MINUTES")

# --- Platform limits --------------------------------------------------------

MAX_SUBMISSION_BYTES = env("MAX_SUBMISSION_BYTES")
ASSESSMENT_WORKER_TIMEOUT_SECONDS = env("ASSESSMENT_WORKER_TIMEOUT_SECONDS")
DATA_UPLOAD_MAX_MEMORY_SIZE = MAX_SUBMISSION_BYTES
FILE_UPLOAD_MAX_MEMORY_SIZE = MAX_SUBMISSION_BYTES

# --- Internationalisation ---------------------------------------------------

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# --- Static and media -------------------------------------------------------

STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# --- Logging ----------------------------------------------------------------

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "{asctime} {levelname} {name} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": env.str("LOG_LEVEL", default="INFO"),
    },
    "loggers": {
        "django.request": {
            "handlers": ["console"],
            "level": "WARNING",
            "propagate": False,
        },
        "skillproof": {
            "handlers": ["console"],
            "level": env.str("LOG_LEVEL", default="INFO"),
            "propagate": False,
        },
    },
}
