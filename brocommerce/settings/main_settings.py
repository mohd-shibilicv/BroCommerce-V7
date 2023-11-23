from pathlib import Path

import django

from django.utils.encoding import force_str

from brocommerce import jazzmin

django.utils.encoding.force_text = force_str

BASE_DIR = Path(__file__).resolve().parent.parent.parent


import os
import environ

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, 'brocommerce/settings/.env'))

JAZZMIN_SETTINGS = jazzmin.JAZZMIN_SETTINGS

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = ['*']

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "allauth.account.auth_backends.AuthenticationBackend",
]

INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "django.contrib.sites",

    "shopadmin.apps.ShopadminConfig",
    "App.apps.AppConfig",
    "App_cart.apps.AppCartConfig",
    "usermanagement.apps.UsermanagementConfig",
    "accounts.apps.AccountsConfig",
    "payment.apps.PaymentConfig",
    "orders.apps.OrdersConfig",
    "home.apps.HomeConfig",
    "checkout.apps.CheckoutConfig",
    "wallet.apps.WalletConfig",
    
    "tailwind",
    "theme",
    "mptt",
    "paypal.standard.ipn",
    "django_extensions",
    "crispy_forms",
    "crispy_tailwind",
    "widget_tweaks",
    "django_filters",
    "allauth",
    "allauth.account",
    "allauth.socialaccount",
    "allauth.socialaccount.providers.github",
    "allauth.socialaccount.providers.google",
]

SITE_ID = 1

TAILWIND_APP_NAME = "theme"

CRISPY_ALLOWED_TEMPLATE_PACKS = "tailwind"

CRISPY_TEMPLATE_PACK = "tailwind"

INTERNAL_IPS = [
    "127.0.0.1",
]

NPM_BIN_PATH = "C:/Program Files/nodejs/npm.cmd"

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = "brocommerce.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "App.context_processors.categories",
                "App.context_processors.user_wishlist",
                "App.context_processors.orders_count",
                "App_cart.context_processors.cart",
            ],
        },
    },
]

WSGI_APPLICATION = "brocommerce.wsgi.application"


DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

SOCIALACCOUNT_PROVIDERS = {
    "google": {
        "APP": {
            "client_id": env('GOOGLE_CLIENT_ID'),
            "secret": env('GOOGLE_CLIENT_SECRET'),
            "key": "",
        },
    },
    "github": {
        "APP": {
            "client_id": str(os.getenv('GITHUB_CLIENT_ID')),
            "secret": str(os.getenv('GITHUB_CLIENT_SECRET')),
        },
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True


STATIC_URL = "static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media/")


DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

ACCOUNT_FORMS = {"login": "accounts.forms.MyCustomLoginForm"}

LOGIN_URL = "account:login"
LOGOUT_URL = "account:logout"
LOGIN_REDIRECT_URL = "App:all_products"
LOGOUT_REDIRECT_URL = "account:login"

BASKET_SESSION_ID = "session_key"

# Custom User Model
AUTH_USER_MODEL = "accounts.Customer"

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_USE_TLS = True
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "mohshibilicv@gmail.com"
EMAIL_HOST_PASSWORD = "ypkjettmaqvczfkg"
EMAIL_PORT = 587

JAZZMIN_SETTINGS = jazzmin.JAZZMIN_SETTINGS
JAZZMIN_UI_TWEAKS = jazzmin.JAZZMIN_UI_TWEAKS

PAYPAL_RECEIVER_EMAIL = "sb-5zcdq27787995@business.example.com"
PAYPAL_TEST = True
