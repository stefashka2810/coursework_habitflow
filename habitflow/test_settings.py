from .settings import *

# Use SQLite for testing
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
    }
}

# Disable any unnecessary services or features during testing
EMAIL_BACKEND = 'django.core.mail.backends.dummy.EmailBackend' 