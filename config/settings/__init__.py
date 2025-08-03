
"""
Django settings package initialization.
This file determines which environment settings to load.
"""

import os
from dotenv import load_dotenv

load_dotenv()

ENVIRONMENT = os.getenv('DJANGO_ENVIRONMENT', 'development')

print(f" Loading Django settings for: {ENVIRONMENT}")


if ENVIRONMENT == 'production':
    try:
        from .production import *
    except ImportError as e:
        from .development import *
        print("Development settings loaded as fallback")
elif ENVIRONMENT == 'development':
    try:
        from .development import *
    except ImportError as e:
        raise
else:
    print(f"⚠️  Unknown environment '{ENVIRONMENT}', using development settings")
    try:
        from .development import *
    except ImportError as e:
        raise

# Debug info
print(f"📍 Django will use environment: {ENVIRONMENT}")
print(f"📍 DEBUG mode: {globals().get('DEBUG', 'Not set')}")
print(f"📍 Database engine: {globals().get('DATABASES', {}).get('default', {}).get('ENGINE', 'Not set')}")