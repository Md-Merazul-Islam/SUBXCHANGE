
import os
from .base import *

DEBUG = os.environ.get('DEBUG', 'False')

# Database: Use PostgreSQL for production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB'),
        'USER': os.environ.get('POSTGRES_USER'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'db'),  # 'db' for Docker
        'PORT': os.environ.get('DB_PORT', '5432'),
        # Performance optimizations
        'CONN_MAX_AGE': 60,
        'OPTIONS': {
            'connect_timeout': 10,
        }
    }
}

# Static files for production
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# CORS: Restrict to your domains only
CORS_ALLOW_ALL_ORIGINS = False

ALLOWED_HOSTS = ["*",'http://165.232.130.130:8001']

CORS_ALLOWED_ORIGINS = [
    'http://165.232.130.130:8001',
]

CSRF_TRUSTED_ORIGINS = [
    'http://165.232.130.130:8001',
]


# rate limiting (throttling)
REST_FRAMEWORK.update({
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.UserRateThrottle',
        'rest_framework.throttling.AnonRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'user': '1000/hour', # An authenticated user can make up to 1000 API requests per hour.
        'anon': '100/hour', #An unauthenticated user can make only 100 requests per hour.
    },
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
})


# Logging configuration for production

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}

# Security headers
X_FRAME_OPTIONS = 'DENY'
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True

print("✅ Production settings loaded")
