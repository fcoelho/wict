from .base import *

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': PROJECT_DIR.child('base.sqlite3'),
    }
}

WSGI_APPLICATION = 'wict.wsgi.dev.application'

SENDFILE_BACKEND = 'sendfile.backends.development'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
