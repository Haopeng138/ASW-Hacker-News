"""
Django settings for hackersNews project.

Generated by 'django-admin startproject' using Django 4.1.2.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-qo8%r-i^fx230%%ucf#xja1x%#q7(97)u)rs92_2te&oy#*32f'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'django.contrib.auth',
    'django.contrib.messages',

    'api.apps.ApiConfig',

    'rest_framework',
    'rest_framework_api_key',

    'homepage.apps.HomepageConfig',
    # Google OAuth Django module
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # providers.google es uno de muchos proveedores de OAuth
    'accounts.apps.AccountsConfig',
    'corsheaders',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    #Cors
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

#CORS_ORIGIN_WHITELIST = (
#'http://localhost:8000',  # for localhost (REACT Default)
#'http://192.168.10.45:3000', # for network
#'http://haopeng138.pythonanywhere.com',
#)


CSRF_TRUSTED_ORIGINS = ["https://sheltered-wave-07620.herokuapp.com"]
ROOT_URLCONF = 'hackersNews.urls'

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

#WSGI_APPLICATION = 'hackersNews.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
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

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_TMP = os.path.join(BASE_DIR,'homepage/static')

os.makedirs(STATIC_TMP,exist_ok=True)
os.makedirs(STATIC_ROOT,exist_ok=True)

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'homepage/static'),
)

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'accounts.HNUser'


STATIC_ROOT = os.path.join(BASE_DIR,'staticfiles')
STATIC_TMP = os.path.join(BASE_DIR,'static')

#STATIC_URL = '/static/'

os.makedirs(STATIC_TMP,exist_ok=True)
os.makedirs(STATIC_ROOT,exist_ok=True)

"""
STATICFILES_DIRS = (
    os.path.join(BASE_DIR,'static'),
)
"""
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Allauth

ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
ACCOUNT_USERNAME_REQUIRED = False       # NOTE: Mirar si ha de ser true


AUTHENTICATION_BACKENDS = [
    #NOTE: Seguramente se tenga que cambiar a un modelo personalizado
    #      que herede de 'django.contrib.auth.backends.BaseBackend'
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend'
]

SOCIALACCOUNT_PROVIDERS = {
    # Google como proveedor de OAuth
    'google': {
        'APP': {
            'client_id': '578655088426-01igiknlmkjp9akmnar7joq499e9254b.apps.googleusercontent.com',
            'secret': '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',
            'key': ''
        },
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': { # Cambiar a 'offline' para hacer referesh de la autentificacion en segundo plano
            'access_type': 'online',
        },
    }
}

# ID para allauth, no se que importancia tiene el numero (Marc)
SITE_ID = 1

ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = True
LOGIN_REDIRECT_URL = '/homepage'
LOGOUT_REDIRECT_URL = '/homepage'

"""
# 'signup' duplicado, lo comento por ahora
ACCOUNT_FORMS = { # Especificar forms personalizados
    'add_email': 'allauth.account.forms.AddEmailForm',
    'change_password': 'allauth.account.forms.ChangePasswordForm',
    'disconnect': 'allauth.socialaccount.forms.DisconnectForm',
    'login': 'allauth.account.forms.LoginForm',
    'reset_password': 'allauth.account.forms.ResetPasswordForm',
    'reset_password_from_key': 'allauth.account.forms.ResetPasswordKeyForm',
    'set_password': 'allauth.account.forms.SetPasswordForm',
    'signup': 'allauth.account.forms.SignupForm',
    'signup': 'allauth.socialaccount.forms.SignupForm',
}
"""

ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

SOCIALACCOUNT_AUTO_SIGNUP = True  # DEF: True

ACCOUNT_ADAPTER = 'accounts.adapters.HN_AccountAdapter'


## Post
PAGE_LIMIT = 30
HOTTEST_DAY_LIMIT = 60


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
   'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAdminUser',
   ),
}

CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_METHODS = (
    'DELETE',
    'GET',
    'POST',
    'PUT',
)

CSRF_TRUSTED_ORIGINS = ['https://*.herokuapp.com',
'https://haopeng138.pythonanywhere.com/']

SECURE_CROSS_ORIGIN_OPENER_POLICY = None
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'apiKey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization'
        }
    },
}
