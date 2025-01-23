"""
Django settings for FoodHub project.

Generated by 'django-admin startproject' using Django 5.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
from dotenv import load_dotenv # type: ignore
import os

import dj_database_url

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-9!q5fc+$lxfn&^4ix+-9%7-+9d+ilmol%t27zv5569%46^_bo#'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": (
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ),
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=1),
}


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',  # For handling cross-origin requests
    'api',
    # 'drf-spectacular',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'corsheaders.middleware.CorsMiddleware',
]

ROOT_URLCONF = 'FoodHub.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'FoodHub.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    # 'default': {
    #     'ENGINE': 'django.db.backends.postgresql',
    #     'NAME': os.getenv('DB_NAME'),
    #     'USER': os.getenv('DB_USER'),
    #     'PASSWORD': os.getenv('DB_PWD'),
    #     'HOST': os.getenv('Db_HOST'),
    #     'PORT': os.getenv('DB_PORT')
    # }

    'default': dj_database_url.config(
        default='postgresql://recipedb_x74k_user:bX6aDPapIrFUkSErgvUNPS4AgR8DJj6M@dpg-cu2j3ndds78s73dtugm0-a.oregon-postgres.render.com/recipedb_x74k',

    )
    
}

# Media settings
MEDIA_URL = '/media/'  # URL to access the uploaded media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')  # Folder where files will be saved


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# # security setting 
# CSRF_COOKIE_SAMESITE = 'strict'
# SESSION_COOKIE_SAMESITE = 'strict'
# CSRF_COOKIE_HTTPONLY = False
# SESSION_COOKIE_HTTPONLY = True
# # For production
# CSRF_COOKIE_HTTPONLY = True
# SESSION_COOKIE_HTTPONLY = True

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",  
    "http://localhost:5174",
    "https://foodhub-156e0.web.app",
]

# REST_FRAMEWORK = {'DEFAULT_SCHEMA_CLASS':'drf-spectacular.openapi.AutoSchema'}

# SPECTACULAR_SETTINGS = {"TITLE":"Foodie Hub Documentation"}

ALLOWED_HOSTS = ['foodiehub-727v.onrender.com', 'localhost', '127.0.0.1']


CORS_ALLOW_ALL_ORIGINS = True


CORS_ALLOW_CREDENTIALS = True