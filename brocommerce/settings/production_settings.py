from .main_settings import *

if not DEBUG:
    ALLOWED_HOSTS = ['127.0.0.1']

    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'brocommercedb',
            'USER': 'brocommercesuper',
            'PASSWORD': 'brocommerceshibilicv',
            'HOST': 'brocommercedb.crjba1wh2thv.eu-north-1.rds.amazonaws.com',
            'PORT': '5432',
        }
    }

    SECURE_SSL_REDIRECT = True

    SESSION_COOKIE_SECURE = True

    CSRF_COOKIE_SECURE = True

    SECURE_BROWSER_XSS_FILTER = True
    
