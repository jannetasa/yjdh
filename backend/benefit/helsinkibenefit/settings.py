import os

import environ
import sentry_sdk
from django.utils.translation import gettext_lazy as _
from sentry_sdk.integrations.django import DjangoIntegration

checkout_dir = environ.Path(__file__) - 2
assert os.path.exists(checkout_dir("manage.py"))

parent_dir = checkout_dir.path("..")
if os.path.isdir(parent_dir("etc")):
    env_file = parent_dir("etc/env")
    default_var_root = environ.Path(parent_dir("var"))
else:
    env_file = checkout_dir(".env")
    default_var_root = environ.Path(checkout_dir("var"))

env = environ.Env(
    DEBUG=(bool, False),
    SECRET_KEY=(str, ""),
    MEDIA_ROOT=(environ.Path(), default_var_root("media")),
    STATIC_ROOT=(environ.Path(), default_var_root("static")),
    MEDIA_URL=(str, "/media/"),
    STATIC_URL=(str, "/static/"),
    ALLOWED_HOSTS=(list, ["*"]),
    USE_X_FORWARDED_HOST=(bool, False),
    DATABASE_URL=(
        str,
        "postgres://benefit:benefit@benefit-db:5434/benefit",
    ),
    CACHE_URL=(str, "locmemcache://"),
    MAIL_MAILGUN_KEY=(str, ""),
    MAIL_MAILGUN_DOMAIN=(str, ""),
    MAIL_MAILGUN_API=(str, ""),
    SENTRY_DSN=(str, ""),
    SENTRY_ENVIRONMENT=(str, ""),
    CORS_ORIGIN_WHITELIST=(list, []),
    CORS_ORIGIN_ALLOW_ALL=(bool, False),
    CSRF_COOKIE_DOMAIN=(str, "localhost"),
    CSRF_TRUSTED_ORIGINS=(list, []),
    YTJ_BASE_URL=(str, "http://avoindata.prh.fi/opendata/tr/v1"),
    YTJ_TIMEOUT=(int, 30),
    MOCK_FLAG=(bool, False),
    # Random 32 bytes AES key, for testing purpose only, DO NOT use the same value in staging/production
    # Always override this value from env variables
    ENCRYPTION_KEY=(
        str,
        "f164ec6bd6fbc4aef5647abc15199da0f9badcc1d2127bde2087ae0d794a9a0b",
    ),
    SOCIAL_SECURITY_NUMBER_HASH_KEY=(
        str,
        "ee235e39ebc238035a6264c063dd829d4b6d2270604b57ee1f463e676ec44669",
    ),
    PREVIOUS_BENEFITS_SOCIAL_SECURITY_NUMBER_HASH_KEY=(
        str,
        "d5c8a2743d726a33dbd637fac39d6f0712dcee4af36142fb4fb15afa17b1d9bf",
    ),
    SESSION_COOKIE_AGE=(int, 60 * 60 * 2),
    OIDC_RP_CLIENT_ID=(str, ""),
    OIDC_RP_CLIENT_SECRET=(str, ""),
    OIDC_OP_BASE_URL=(str, ""),
    LOGIN_REDIRECT_URL=(str, "/"),
    LOGIN_REDIRECT_URL_FAILURE=(str, "/"),
    ADFS_LOGIN_REDIRECT_URL=(str, "/"),
    ADFS_LOGIN_REDIRECT_URL_FAILURE=(str, "/"),
    EAUTHORIZATIONS_BASE_URL=(str, "https://asiointivaltuustarkastus.test.suomi.fi"),
    EAUTHORIZATIONS_CLIENT_ID=(str, "sample_client_id"),
    EAUTHORIZATIONS_CLIENT_SECRET=(str, ""),
    EAUTHORIZATIONS_API_OAUTH_SECRET=(str, ""),
    ADFS_CLIENT_ID=(str, "client_id"),
    ADFS_CLIENT_SECRET=(str, "client_secret"),
    ADFS_TENANT_ID=(str, "tenant_id"),
    ADFS_CONTROLLER_GROUP_UUIDS=(list, []),
    DEFAULT_FILE_STORAGE=(str, "django.core.files.storage.FileSystemStorage"),
    AZURE_ACCOUNT_NAME=(str, ""),
    AZURE_ACCOUNT_KEY=(str, ""),
    AZURE_CONTAINER=(str, ""),
    AZURE_URL_EXPIRATION_SECS=(int, 900),
    MINIMUM_WORKING_HOURS_PER_WEEK=(int, 18),
    AUDIT_LOG_ORIGIN=(str, "helsinki-benefit-api"),
    ELASTICSEARCH_APP_AUDIT_LOG_INDEX=(str, "helsinki_benefit_audit_log"),
    ELASTICSEARCH_CLOUD_ID=(str, ""),
    ELASTICSEARCH_API_ID=(str, ""),
    ELASTICSEARCH_API_KEY=(str, ""),
    CLEAR_AUDIT_LOG_ENTRIES=(bool, False),
    ENABLE_SEND_AUDIT_LOG=(bool, False),
    WKHTMLTOPDF_BIN=(str, "/usr/bin/wkhtmltopdf"),
    DISABLE_AUTHENTICATION=(bool, False),
    DUMMY_COMPANY_FORM=(str, "OY"),
    TERMS_OF_SERVICE_SESSION_KEY=(str, "_tos_session"),
    ENABLE_DEBUG_ENV=(bool, False),
)
if os.path.exists(env_file):
    env.read_env(env_file)

BASE_DIR = str(checkout_dir)

DEBUG = env.bool("DEBUG")
SECRET_KEY = env.str("SECRET_KEY")
if DEBUG and not SECRET_KEY:
    SECRET_KEY = "xxx"
ENCRYPTION_KEY = env.str("ENCRYPTION_KEY")
SOCIAL_SECURITY_NUMBER_HASH_KEY = env.str("SOCIAL_SECURITY_NUMBER_HASH_KEY")
PREVIOUS_BENEFITS_SOCIAL_SECURITY_NUMBER_HASH_KEY = env.str(
    "PREVIOUS_BENEFITS_SOCIAL_SECURITY_NUMBER_HASH_KEY"
)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
USE_X_FORWARDED_HOST = env.bool("USE_X_FORWARDED_HOST")

DATABASES = {"default": env.db()}

CACHES = {"default": env.cache()}

sentry_sdk.init(
    dsn=env.str("SENTRY_DSN"),
    release="n/a",
    environment=env("SENTRY_ENVIRONMENT"),
    integrations=[DjangoIntegration()],
)

MEDIA_ROOT = env("MEDIA_ROOT")
STATIC_ROOT = env("STATIC_ROOT")
MEDIA_URL = env.str("MEDIA_URL")
STATIC_URL = env.str("STATIC_URL")

ROOT_URLCONF = "helsinkibenefit.urls"
WSGI_APPLICATION = "helsinkibenefit.wsgi.application"

LANGUAGE_CODE = "fi"
LANGUAGES = (("fi", _("Finnish")), ("en", _("English")), ("sv", _("Swedish")))
TIME_ZONE = "Europe/Helsinki"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, "locale"),)

INSTALLED_APPS = [
    # shared apps
    "shared.oidc",
    "shared.audit_log",
    # local apps
    "users.apps.AppConfig",
    "companies",
    "applications.apps.AppConfig",
    "terms.apps.AppConfig",
    "calculator.apps.AppConfig",
    # libraries
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "django_filters",
    "drf_spectacular",  # OpenAPI documentation
    "phonenumber_field",
    "django_extensions",
    "encrypted_fields",
    "mozilla_django_oidc",
    "django_auth_adfs",
]

AUTH_USER_MODEL = "users.User"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

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
            ]
        },
    }
]

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_WHITELIST = env.list("CORS_ORIGIN_WHITELIST")
CORS_ORIGIN_ALLOW_ALL = env.bool("CORS_ORIGIN_ALLOW_ALL")
CSRF_COOKIE_DOMAIN = env.str("CSRF_COOKIE_DOMAIN")
CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")

# Audit logging
AUDIT_LOG_ORIGIN = env.str("AUDIT_LOG_ORIGIN")
CLEAR_AUDIT_LOG_ENTRIES = env.bool("CLEAR_AUDIT_LOG_ENTRIES")
ELASTICSEARCH_APP_AUDIT_LOG_INDEX = env("ELASTICSEARCH_APP_AUDIT_LOG_INDEX")
ELASTICSEARCH_CLOUD_ID = env("ELASTICSEARCH_CLOUD_ID")
ELASTICSEARCH_API_ID = env("ELASTICSEARCH_API_ID")
ELASTICSEARCH_API_KEY = env("ELASTICSEARCH_API_KEY")
ENABLE_SEND_AUDIT_LOG = env("ENABLE_SEND_AUDIT_LOG")

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {"console": {"class": "logging.StreamHandler"}},
    "loggers": {"django": {"handlers": ["console"], "level": "ERROR"}},
}

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": (
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ),
    "DEFAULT_AUTHENTICATION_CLASSES": ["shared.oidc.auth.EAuthRestAuthentication"],
    "DEFAULT_PERMISSION_CLASSES": [
        "common.permissions.BFIsAuthenticated",
    ],
    "TEST_REQUEST_DEFAULT_FORMAT": "json",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}  # TODO: Replace with actual authentication & permissions.

SPECTACULAR_SETTINGS = {
    "TITLE": "Helsinki Benefit API",
    "ENUM_NAME_OVERRIDES": {
        "AvailableBenefitTypesEnum": "applications.enums.BenefitType",
    },
    "DESCRIPTION": """REST API for Helsinki Benefit application management

# Authentication methods
<SecurityDefinitions />
""",
    "VERSION": "0.0.1",
    "EXTERNAL_DOCS": {
        "description": "Helsinki benefit / YJDH repository in GitHub",
        "url": "https://github.com/City-of-Helsinki/yjdh",
    },
}

PHONENUMBER_DB_FORMAT = "NATIONAL"
PHONENUMBER_DEFAULT_REGION = "FI"

YTJ_BASE_URL = env.str("YTJ_BASE_URL")
YTJ_TIMEOUT = env.int("YTJ_TIMEOUT")

# Mock flag for testing purposes
MOCK_FLAG = env.bool("MOCK_FLAG")
DUMMY_COMPANY_FORM = env.str("DUMMY_COMPANY_FORM")
ENABLE_DEBUG_ENV = env.bool("ENABLE_DEBUG_ENV")

# Authentication settings begin
SESSION_COOKIE_AGE = env.int("SESSION_COOKIE_AGE")
SESSION_COOKIE_SECURE = True

TERMS_OF_SERVICE_SESSION_KEY = env.str("TERMS_OF_SERVICE_SESSION_KEY")

AUTHENTICATION_BACKENDS = (
    "shared.oidc.auth.HelsinkiOIDCAuthenticationBackend",
    # Temporary disable ADFS
    # "shared.azure_adfs.auth.HelsinkiAdfsAuthCodeBackend",
    "django.contrib.auth.backends.ModelBackend",
)

DISABLE_AUTHENTICATION = env.bool("DISABLE_AUTHENTICATION")

OIDC_RP_SIGN_ALGO = "RS256"
OIDC_RP_SCOPES = "openid profile"

OIDC_RP_CLIENT_ID = env.str("OIDC_RP_CLIENT_ID")
OIDC_RP_CLIENT_SECRET = env.str("OIDC_RP_CLIENT_SECRET")

OIDC_OP_BASE_URL = env.str("OIDC_OP_BASE_URL")
OIDC_OP_AUTHORIZATION_ENDPOINT = f"{OIDC_OP_BASE_URL}/auth"
OIDC_OP_TOKEN_ENDPOINT = f"{OIDC_OP_BASE_URL}/token"
OIDC_OP_USER_ENDPOINT = f"{OIDC_OP_BASE_URL}/userinfo"
OIDC_OP_JWKS_ENDPOINT = f"{OIDC_OP_BASE_URL}/certs"
OIDC_OP_LOGOUT_ENDPOINT = f"{OIDC_OP_BASE_URL}/logout"

LOGIN_REDIRECT_URL = env.str("LOGIN_REDIRECT_URL")
LOGIN_REDIRECT_URL_FAILURE = env.str("LOGIN_REDIRECT_URL_FAILURE")

EAUTHORIZATIONS_BASE_URL = env.str("EAUTHORIZATIONS_BASE_URL")
EAUTHORIZATIONS_CLIENT_ID = env.str("EAUTHORIZATIONS_CLIENT_ID")
EAUTHORIZATIONS_CLIENT_SECRET = env.str("EAUTHORIZATIONS_CLIENT_SECRET")
EAUTHORIZATIONS_API_OAUTH_SECRET = env.str("EAUTHORIZATIONS_API_OAUTH_SECRET")

# Azure ADFS
LOGIN_URL = "django_auth_adfs:login"

ADFS_CLIENT_ID = env.str("ADFS_CLIENT_ID") or "client_id"
ADFS_CLIENT_SECRET = env.str("ADFS_CLIENT_SECRET") or "client_secret"
ADFS_TENANT_ID = env.str("ADFS_TENANT_ID") or "tenant_id"

# https://django-auth-adfs.readthedocs.io/en/latest/azure_ad_config_guide.html#step-2-configuring-settings-py
AUTH_ADFS = {
    "AUDIENCE": ADFS_CLIENT_ID,
    "CLIENT_ID": ADFS_CLIENT_ID,
    "CLIENT_SECRET": ADFS_CLIENT_SECRET,
    "CLAIM_MAPPING": {"email": "email"},
    "USERNAME_CLAIM": "oid",
    "TENANT_ID": ADFS_TENANT_ID,
    "RELYING_PARTY_ID": ADFS_CLIENT_ID,
}

ADFS_LOGIN_REDIRECT_URL = env.str("ADFS_LOGIN_REDIRECT_URL")
ADFS_LOGIN_REDIRECT_URL_FAILURE = env.str("ADFS_LOGIN_REDIRECT_URL_FAILURE")

# Authentication settings end

FIELD_ENCRYPTION_KEYS = [ENCRYPTION_KEY]

# Django storages
DEFAULT_FILE_STORAGE = env("DEFAULT_FILE_STORAGE")

AZURE_ACCOUNT_NAME = env("AZURE_ACCOUNT_NAME")
AZURE_ACCOUNT_KEY = env("AZURE_ACCOUNT_KEY")
AZURE_CONTAINER = env("AZURE_CONTAINER")
AZURE_URL_EXPIRATION_SECS = env("AZURE_URL_EXPIRATION_SECS")  # default 900s

MAX_UPLOAD_SIZE = 10485760  # 10MB
MINIMUM_WORKING_HOURS_PER_WEEK = env("MINIMUM_WORKING_HOURS_PER_WEEK")

WKHTMLTOPDF_BIN = env("WKHTMLTOPDF_BIN")

# local_settings.py can be used to override environment-specific settings
# like database and email that differ between development and production.
local_settings_path = os.path.join(checkout_dir(), "local_settings.py")
if os.path.exists(local_settings_path):
    with open(local_settings_path) as fp:
        code = compile(fp.read(), local_settings_path, "exec")
    exec(code, globals(), locals())
