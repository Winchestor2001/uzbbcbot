"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 5.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import os
from pathlib import Path
import sys
from environs import Env
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(os.path.join(BASE_DIR, "apps"))
env = Env()
env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG")

CSRF_TRUSTED_ORIGINS = env.list("CSRF_TRUSTED_ORIGINS")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
DOMAIN = env.str("DOMAIN")

# Application definition

INSTALLED_APPS = [
    # 'jazzmin',
    'unfold',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bot_api.apps.BotApiConfig',
    'celery_tasks.apps.CeleryTasksConfig',
    'comments.apps.CommentsConfig',
    'colorfield',
    'rest_framework',
]


UNFOLD = {
    "SITE_TITLE": "App",
    "SITE_HEADER": "App",
    "DASHBOARD_CALLBACK": "bot_api.views.dashboard_callback",
}


LANGUAGES = [
    ('uz', _('Uzbek')),
    ('ru', _('Russian')),
    ('en', _('English')),
]

LOCALE_PATHS = [BASE_DIR/'locale']

MODELTRANSLATION_DEFAULT_LANGUAGE = 'uz'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env.str("POSTGRES_DB"),
            'USER': env.str("POSTGRES_USER"),
            'PASSWORD': env.str("POSTGRES_PASSWORD"),
            'HOST': env.str("POSTGRES_HOST"),
            'PORT': env.int("POSTGRES_PORT"),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Tashkent'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

if DEBUG:
    STATICFILES_DIRS = [
        BASE_DIR / 'static',
    ]
else:
    STATIC_ROOT = BASE_DIR / 'static'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

JAZZMIN_SETTINGS = {
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user-shield",
        "auth.Group": "fas fa-users",
        "bot_api.tguser": "fas fa-user",
        "bot_api.servicerating": "fas fa-star",
        "bot_api.productrating": "fas fa-star",
        "bot_api.region": "fas fa-city",
        "bot_api.professional": "fas fa-user-tie",
        "bot_api.productcategory": "fab fa-product-hunt",
        "bot_api.servicecategory": "fas fa-copyright",
        "bot_api.productdetail": "fas fa-info",
        "bot_api.servicestuff": "fas fa-id-badge",
        "bot_api.market": "fas fa-store",
        "bot_api.aboutbot": "fas fa-tools",
    },
    "hide_models": ['auth.Group'],
}


# Celery
REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.str("REDIS_PORT")
CELERY_BROKER_URL = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
CELERY_ACCEPT_CONTENT = env.list("CELERY_ACCEPT_CONTENT")
CELERY_TASK_SERIALIZER = env.str("CELERY_TASK_SERIALIZER")
CELERY_RESULT_SERIALIZER = env.str("CELERY_RESULT_SERIALIZER")


CORS_ALLOW_ALL_ORIGINS = True


log_path = env.str('WEB_LOG_PATH', default=str(BASE_DIR / 'logs/web_error.log'))

log_dir = os.path.dirname(log_path)
os.makedirs(log_dir, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'formatter': 'verbose',
            'filename': log_path,
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}

DB_LANGUAGES = (
    ('uz', 'uz'),
    ('ru', 'ru'),
    ('en', 'en'),
)
