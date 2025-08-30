from .base import *

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "chukticketingsystem.com", "www.chukticketingsystem.com"]
#ALLOWED_HOSTS  = ["*"]

# CORS settings for frontend integration
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",  # Next.js development server
    "http://127.0.0.1:3000",
    "https://rphub.vercel.app",  # Vercel deployment
    "https://repairhub-delta.vercel.app",  # Vercel deployment (new domain)
]

CORS_ALLOW_CREDENTIALS = True  # Allow cookies in cross-origin requests
CORS_ALLOW_ALL_ORIGINS = False  # Disable wildcard (*) for security

# Additional CORS headers
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

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / "static",  
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'chukticketingsystem_dev',
        'USER': 'postgres',
        'PASSWORD': 'godsp',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# CORS_ALLOW_CREDENTIALS = True  # Allow cookies in cross-origin requests
# CORS_ALLOW_ALL_ORIGINS = False  # Disable wildcard (*) to allow credentials
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:8000",  
#     "http://127.0.0.1:8000",
# ]

# # CSRF Settings (Ensures requests from frontend are not blocked)
# CSRF_COOKIE_SAMESITE = "Lax"  # Allows CSRF cookies for same-site requests
# CSRF_COOKIE_SECURE = False  # Disable for local development (Enable in production)

# # Session Settings (Ensures authentication persistence)
# SESSION_COOKIE_SAMESITE = "None"  # Allows cookies for same-site requests
# # Enable Django session storage
# SESSION_ENGINE = "django.contrib.sessions.backends.db"  # Store sessions in database
# SESSION_COOKIE_NAME = "sessionid"  # Default cookie name for Django sessions
# SESSION_COOKIE_AGE = 1209600  # (2 weeks) Session expiry time
# SESSION_SAVE_EVERY_REQUEST = True  # Save session on every request
# SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # Keep session active after closing browser
# SESSION_COOKIE_SECURE = False  # Set to True if using HTTPS


# Custom cookies (e.g., refresh_token, access_token)

ACCESS_TOKEN_COOKIE_NAME = 'access_token'
REFRESH_TOKEN_COOKIE_NAME = 'refresh_token'



# Paypal sandbox configuration settings
PAYPAL_MODE = 'sandbox'  
PAYPAL_CLIENT_ID = 'AVqcrSsLrrQMuxDxxQnXBiCP14ZPyKWqtOSJq4NYWYFHwVj7jipCoyueyH9l3dbtTtAyjcXpGiRi651s'
PAYPAL_SECRET = 'EB7mcNZ9rqtKhr3Sppm3a45QfQu_LuYYAsl65M7B8XK-QbUKMgSCDfsvPeJubM-lsz8rVz-cH0opss6-'



