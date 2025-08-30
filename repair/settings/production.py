

from .base import * 



DEBUG = True
# ALLOWED_HOSTS = list (os.getenv("ALLOWED_HOSTS", ["185.113.249.94","firststore.codemeduck.com"]))

ALLOWED_HOSTS = ['127.0.0.1',"102.212.247.252","chukticketingsystem.com",'www.chukticketingsystem.com', '.vercel.app']

INSTALLED_APPS += ['django.contrib.postgres']


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'static'  # Where static files will be collected

# CORS settings for production
CORS_ALLOWED_ORIGINS = [
    "https://rphub.vercel.app",  # Your Vercel deployment
    "https://repairhub-delta.vercel.app",  # Additional Vercel deployment
    "https://chukticketingsystem.com",
    "https://www.chukticketingsystem.com",
]

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

CSRF_TRUSTED_ORIGINS = [
    'https://chukticketingsystem.com',
    'https://www.chukticketingsystem.com',
    'https://rphub.vercel.app',  # Add Vercel deployment
    # If you're using HTTP during development or without SSL for some reason:
    'http://chukticketingsystem.com',
    'http://www.chukticketingsystem.com',
    # If you access via IP directly for testing, add it:
    # 'http://YOUR_SERVER_IP_ADDRESS',
    # 'https://YOUR_SERVER_IP_ADDRESS',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv("DB_NAME", "repair_db"),
        'USER': os.getenv("DB_USER", "repair"),
        'PASSWORD': os.getenv("DB_PASSWORD","Captain@248"),
        'HOST': os.getenv("DB_HOST","127.0.0.1"),
        'PORT': os.getenv("DB_PORT", "5432"),
        'OPTIONS': {
            'sslmode': 'disable',
        }
    }
}

CORS_ALLOW_CREDENTIALS = True  # Allow sending cookies with requests

# CSRF settings
CSRF_COOKIE_SAMESITE = 'Strict'  
CSRF_COOKIE_SECURE = True  # Required for SameSite=None

# Session settings
SESSION_COOKIE_SAMESITE = 'None'
SESSION_COOKIE_SECURE = True

# Security settings
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# PayPal Live Configuration
PAYPAL_MODE = 'live'
PAYPAL_CLIENT_ID = os.getenv("PAYPAL_CLIENT_ID", default="")
PAYPAL_SECRET = os.getenv("PAYPAL_SECRET", default="")

# # sendgrid SMTP Settings
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = "smtp.sendgrid.net"
# EMAIL_PORT = 587
# EMAIL_USE_TLS = True
# EMAIL_HOST_USER = "apikey"
# EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD","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")
# DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "support@computuerhubuk.com")
# EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", 30))


# GMAIL SMTP Settings
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER","chuktsystem@gmail.com")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD","vqgkfgynjfuzplrm")
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "support@computuerhubuk.com")
EMAIL_TIMEOUT = int(os.getenv("EMAIL_TIMEOUT", 30))


# Celery Settings
CELERY_BROKER_URL = os.getenv("CELERY_BROKER_URL", "amqp://guest:guest@127.0.0.1:5672//")
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_TASK_RETRY_POLICY = {
    'max_retries': 3,
    'interval_start': 0,
    'interval_step': 2,
    'interval_max': 10,
}



BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_FILE = BASE_DIR / "logs_file" / "production.log"

# Ensure the logs directory exists
LOG_FILE.parent.mkdir(exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
        'level': 'WARNING',
        'class': 'logging.handlers.RotatingFileHandler',
        'filename': LOG_FILE,
        'maxBytes': 1024 * 1024 * 5,  # Max file size of 5MB
        'backupCount': 3,  # Keep the last 3 log files
        'formatter': 'verbose',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': True,
        },
    },
}



# PayPal Configuration
# PAYPAL_MODE=live
# PAYPAL_CLIENT_ID=your_paypal_client_id
# PAYPAL_SECRET=your_paypal_secret
