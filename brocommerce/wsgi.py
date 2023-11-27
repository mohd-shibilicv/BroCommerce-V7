import os
import environ

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, 'brocommerce/settings/.env'))

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brocommerce.settings.main_settings')

application = get_wsgi_application()
