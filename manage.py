#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import environ

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, 'brocommerce/settings/.env'))

def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'brocommerce.settings.main_settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
