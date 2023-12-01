"""
Django settings for activation project.

Generated by 'django-admin startproject' using Django 4.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
from datetime import timedelta
import os
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-*blsn=irlbndmf1!vyt07xdb7!51r#i#k-2j)j-4)k6(s&8z8$'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
# DEBUG = True

# ALLOWED_HOSTS = ['.vercel.app']
ALLOWED_HOSTS = ["*"]
AUTH_USER_MODEL = 'authenticate.User'


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authenticate',
    'transaction',
    'rest_framework',
    'drf_yasg',
    'corsheaders'
]

SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS':{
        'Bearer':{
            'type':'apiKey',
            'name':'Authorization',
            'in':'header'
        }
    }
}

REST_FRAMEWORK = {
    'NON_FIELD_ERRORS_KEY' : "error",
    'DEFAULT_PERMISSION_CLASSES' : [
        'rest_framework.permissions.IsAuthenticated'
    ],
    
    'DEFAULT_AUTHENTICATION_CLASSES' : [
        'rest_framework_simplejwt.authentication.JWTAuthentication'
    ]
}


SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=30),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    # other JWT settings...
}

JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': timedelta(hours=1),
    'JWT_REFRESH_EXPIRATION_DELTA': timedelta(days=7),  # Set the expiration time for the refresh token
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_ORIGINS = ['*']


ROOT_URLCONF = 'activation.urls'

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

WSGI_APPLICATION = 'activation.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
DATABASES = {
    'default': dj_database_url.parse("postgres://signup_otp_user:IjkJKxbwlvA1ETdkz2zbTn5VCqTtVSEU@dpg-cli7nhfjc5ks73eqpbrg-a.oregon-postgres.render.com/signup_otp")
    }




# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/

# STATIC_ROOT = BASE_DIR / 'static/'
# MEDIA_ROOT = BASE_DIR / 'media/'
STATIC_URL = 'static/'
MEDIA_URL = '/media/'

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

