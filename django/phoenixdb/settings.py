## @package settings
#  Django project settings for the 'phoenixdb' application.
#  This module configures settings like database connections, installed applications,
#  middleware, templates, and more for a Django web application.

import os
from pathlib import Path

## @var BASE_DIR
#  Absolute path to the base directory of the project.
#  This is used to define paths to various configuration directories.
BASE_DIR = Path(__file__).resolve().parent.parent

## @var SECRET_KEY
#  Secret key for the Django application, typically used for cryptographic signing.
#  This key is fetched from the environment variables, with a fallback default if not set.
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')

## @var DEBUG
#  Boolean flag indicating if the application is running in debug mode.
#  Debug mode provides detailed error pages and other development aids.
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

## @var ALLOWED_HOSTS
#  List of host/domain names that this Django site can serve.
#  This is used for security measures to prevent HTTP Host header attacks.
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

## @var INSTALLED_APPS
#  List of applications that are enabled in this Django instance.
#  Each application makes Django capable of handling different web functionalities.
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
]

## @var MIDDLEWARE
#  List of middleware to handle requests during response and request phases.
#  Middleware are hooks into Django's request/response processing.
MIDDLEWARE = [
    'django.middleware.locale.LocaleMiddleware'
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.RoleBasedAccessMiddleware',
]


## @var ROOT_URLCONF
#  A string representing the full Python import path to your root URLconf.
#  This tells Django where to find the URL configuration for the project.
ROOT_URLCONF = 'phoenixdb.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'accounts/templates', BASE_DIR / 'core/templates'],
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

## @var DATABASES
#  Database configuration.
#  Specifies the database engine and connection details fetched from environment variables.
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': os.environ.get('DB_PORT'),
    }
}

## @var AUTH_PASSWORD_VALIDATORS
#  Configuration for password validation.
#  Specifies the validators that are used to check the strength and validity of user passwords.
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

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

LANGUAGE_CODE = 'ru'

## @var TIME_ZONE
#  Default time zone for the Django application.
TIME_ZONE = 'UTC'

## @var USE_I18N
#  Boolean indicating whether Django’s translation system should be enabled.
USE_I18N = True

## @var USE_L10N
#  Boolean indicating whether localized formatting of data will be enabled by default.
USE_L10N = True

## @var USE_TZ
#  Boolean indicating whether Django will use timezone-aware datetimes.
USE_TZ = True

## @var STATIC_URL
#  URL to use when referring to static files located in STATIC_ROOT.
STATIC_URL = '/static/'

## @var STATIC_ROOT
#  The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = BASE_DIR / 'core' / 'static'

## @var MEDIA_URL
#  URL that handles the media served from MEDIA_ROOT, used for managing stored media.
MEDIA_URL = '/media/'

## @var MEDIA_ROOT
#  The absolute path to the directory where all uploaded media files are stored.
MEDIA_ROOT = BASE_DIR / 'media'

LOGIN_REDIRECT_URL = '/tutor/'
LOGOUT_REDIRECT_URL = '/login/'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'app.middleware.RoleBasedAccessMiddleware',  # Добавляем наше кастомное middleware
]

## @var DEFAULT_AUTO_FIELD
#  The default type of primary key to use for new models if the model doesn’t explicitly specify.
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

