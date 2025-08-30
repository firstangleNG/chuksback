import os

ENVIRONMENT = os.getenv("DJANGO_ENV", "local")  # Default to local for development

if ENVIRONMENT == "production":
    from .production import *
else:
    from .local import *
