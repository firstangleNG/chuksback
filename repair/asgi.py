

import os

from django.core.asgi import get_asgi_application

ENVIRONMENT = os.getenv("DJANGO_ENV", "production")  # Default to production
# Set the Django settings module based on the environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", f"repair.settings.{ENVIRONMENT}")

application = get_asgi_application()
