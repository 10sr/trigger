"""
Django settings for proj project.

Generated by 'django-admin startproject' using Django 2.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import logging

from typing import List

_logger = logging.getLogger(__name__)


def _getenv(name: str, default: str = "", fatal_on_empty: bool = False) -> str:
    val = os.environ.get(name, "")
    if val == "" and fatal_on_empty:
        raise KeyError(f"{name} is empty")
    if val == "":
        _logger.warning(f'{name} is empty, resort to default value: "{default}"')
    return val or default


is_prod = _getenv("TRIGGER_ENV") == "prod"

# Named URL Pattern
LOGIN_URL = "login"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = _getenv(
    "TRIGGER_SECRET_KEY",
    "!aw%su!m5-j1^d+x@r5x)0_a@bx%tjrz&4)y$$n65r%e^3hc+a",
    fatal_on_empty=is_prod,
)

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = not is_prod

ALLOWED_HOSTS: List[str] = []


# Application definition

INSTALLED_APPS = [
    # Do not forget to add app or django cannot find templates!
    "trigger.apps.TriggerConfig",
    "proj.manageproj.apps.AppConfig",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "proj.urls"

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

WSGI_APPLICATION = "proj.wsgi.application"


# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": _getenv("TRIGGER_SQLITE3", "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = "/static/"


# trigger specific

TRIGGER_PUSHBULLET_TOKEN = _getenv("TRIGGER_PUSHBULLET_TOKEN")
