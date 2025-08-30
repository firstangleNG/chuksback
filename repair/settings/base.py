from pathlib import Path
import os
import environ
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# 
DJANGO_ENV = os.getenv("DJANGO_ENV", "production")

if DJANGO_ENV == "production":# Production mode (Variables set in systemd)
    DEBUG = os.getenv("DEBUG", "False").lower() in ["true", "1"]
    SECRET_KEY = os.getenv("DJANGO_SECRET_KEY","pSdjtqf_nOySMM9oEqXhOY-2eop641sw6HljbdjdcsUfI1s2kFTIOsdPV0tMxJjNSmi7vUyvr4")

     # Ensure SECRET_KEY is set
    if not SECRET_KEY:
        raise RuntimeError("DJANGO_SECRET_KEY environment variable is required in production")
else:  
    env = environ.Env(DEBUG=(bool, False))
    environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
    DEBUG = env.bool("DEBUG", default=False)
    SECRET_KEY = env("SECRET_KEY")
    



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'corsheaders',  # Added for CORS support
    #custom apps
    'users',
    'repairs',
    'invoice',
    'inventory',
    # 'payments',
    # 'notifications',
    'logs',
    "customers",
    'dashboard',

]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Must be at the top
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'users.backends.EmailAuthBackend',  # Enable email-based login',
    'django.contrib.auth.backends.ModelBackend',  # Fallback to default backend
]


ROOT_URLCONF = 'repair.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR /'templates'],
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

WSGI_APPLICATION = 'repair.wsgi.application'




# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Africa/Lagos'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/


# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES':['rest_framework_simplejwt.authentication.JWTAuthentication',],

    'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.AllowAny',],

    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ]

}