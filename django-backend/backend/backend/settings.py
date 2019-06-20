from pathlib import Path

from dj_database_url import parse as parse_db_url
from prettyconf import config
# from corsheaders.defaults import default_headers


# Project Structure
PROJECT_NAME = "backend"
BASE_DIR = Path(__file__).absolute().parents[2]

# Debug & Development
DEBUG = config("DEBUG", default=False, cast=config.boolean)
LOG_LEVEL = config("LOG_LEVEL", default='WARNING')

# Database
DATABASES = {
    'default': config('DATABASE_URL', cast=parse_db_url),
}

# always connected:
DATABASES['default']['CONN_MAX_AGE'] = config("CONN_MAX_AGE", cast=config.eval, default="None")
DATABASES['default']['TEST'] = {'NAME': config('TEST_DATABASE_NAME', default=None)}

# DATABASE_ROUTERS = ['backend.dbrouter.Router']

# Security & Signup/Signin
ALLOWED_HOSTS = config("ALLOWED_HOSTS", default="*", cast=config.list)
SECRET_KEY = config("SECRET_KEY")


# i18n & l10n
TIME_ZONE = "UTC"
USE_I18N = False
USE_L10N = False
USE_TZ = False
LANGUAGE_CODE = "en-us"

# Miscelaneous
ROOT_URLCONF = "{}.urls".format(PROJECT_NAME)
WSGI_APPLICATION = "{}.wsgi.application".format(PROJECT_NAME)
LOG_REQUEST_ID_HEADER = "HTTP_X_REQUEST_ID"

# Application
MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

INSTALLED_APPS = (
    'django.contrib.postgres',

    'raven.contrib.django.raven_compat',

    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'jet',
    'django.contrib.admin',
    'django_extensions',
    'corsheaders',

    # 'apps.',
)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages'
            ]
        },
    },
]

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'ERROR',
            'class': 'logging.StreamHandler',
        }
    },
    'root': {
        'level': 'INFO',
        'handlers': ['console']
    },
}

CACHES = {
    'default': {
        'BACKEND': config('CACHE_BACKEND', default='django.core.cache.backends.dummy.DummyCache')
    }
}

# CORS:
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = default_headers + (
    'x-username', 'x-password',
)

# Static files / Whitenoise
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Jet (contrib.admin theme)
# JET_DEFAULT_THEME = "light-blue"
