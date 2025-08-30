
import os

from django.core.wsgi import get_wsgi_application

ENVIRONMENT = os.getenv("DJANGO_ENV", "production")  # Default to production
# Set the Django settings module based on the environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "repair.settings.production")

application = get_wsgi_application()
