"""
Django settings for megano project.

Generated by 'django-admin startproject' using Django 4.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""
import os
from pathlib import Path

from src.config import SECRET_KEY as _SECRET_KEY
from src.config import (
    DB_HOST,
    DB_NAME,
    DB_USER,
    DB_PASS,
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = _SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'frontend',
    'rest_framework',
    'rest_framework.authtoken',  # Проверка токенов для аутентификации пользователя
    "src.api_user.apps.AppUserConfig",
    "src.api_shop.apps.AppShopConfig",
    'drf_yasg',  # Документация Swagger
    "django_cleanup.apps.CleanupConfig",  # Очистка файлов при удалении записи
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.megano.urls'

REST_FRAMEWORK = {
    # Пагинация
    # 'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    # 'DEFAULT_PAGINATION_CLASS': 'src.megano.utils.pagination.CustomPagination',
    # 'PAGE_SIZE': 1,

    # Аутентификация
    'DEFAULT_AUTHENTICATION_CLASSES': [
        # 'rest_framework.authentication.BasicAuthentication',
        # TODO Попробовать с этим
        'rest_framework.authentication.SessionAuthentication',
        # 'rest_framework.authentication.TokenAuthentication',
    ],

    # Проверка прав (аутентификации)
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAuthenticated',
    # ]
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
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

CASHES = {
    "default": {
        # Кэширование в ОЗУ
        "BACKEND": "django.core.cache.backends.locmem.LocMemCache",
        "LOCATION": "unique-snowflake",
        "TIMEOUT": 60 * 60 * 24,  # Кэширование на сутки
        "OPTIONS": {"MAX_ENTRIES": 500},
    }
}

WSGI_APPLICATION = 'src.megano.wsgi.application'

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "color": {
            "()": "colorlog.ColoredFormatter",
            "format": "%(log_color)s%(asctime)-8s %(levelname)s - %(name)s.py | func:%(funcName)s (%(lineno)s) - %(message)s",
            "log_colors": {
                "DEBUG": "white",
                "INFO": "green",
                "WARNING": "yellow",
                "ERROR": "red",
                "CRITICAL": "bold_red",
            },
        }
    },
    "handlers": {
        "console": {"class": "logging.StreamHandler", "formatter": "color"},
    },
    "root": {
        "handlers": ["console"],
        "level": "DEBUG",
    },
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# TODO Нужно ли указывать хост при запуске в Docker?
DATABASES = {
    'default': {
        'ENGINE': 'mysql.connector.django',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
    },
}


# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "en-us"
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATICFILES_DIRS = (os.path.join(BASE_DIR, "src", "static"),)

# Директория для сбора статики командой collectstatic
STATIC_ROOT = os.path.join(
    BASE_DIR, "src", "staticfiles"
)

# MEDIA_URL = "/media/"
MEDIA_URL = "/media/"
# Сохраняем файлы в директорию с фронтендом
# MEDIA_ROOT = os.path.join(BASE_DIR, "frontend")
MEDIA_ROOT = BASE_DIR / 'frontend'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
