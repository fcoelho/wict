from unipath import Path

PROJECT_DIR = Path(__file__).ancestor(3)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

TIME_ZONE = 'America/Sao_Paulo'
LANGUAGE_CODE = 'pt-BR'

USE_I18N = True
USE_L10N = True
USE_TZ = True

MEDIA_ROOT = PROJECT_DIR.child('media')
MEDIA_URL = '/media/'

STATIC_ROOT = PROJECT_DIR.child('static')
STATIC_URL = '/static/'

SECRET_KEY = 'gwxr4yc-*@85$#9s@uh268y7c2xxad1+#g+n*$hk9j%gihpo2r'

ROOT_URLCONF = 'wict.urls'

INSTALLED_APPS = (
	# Django contrib apps
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
	# Thirdy party apps
	'signup',
	'sendfile',
	# Wict apps
	'website',
)

AUTH_USER_MODEL = 'website.WictUser'
SIGNUP_FORM_CLASS = 'website.forms.UserSignUpForm'

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

ACCOUNT_ACTIVATION_DAYS = 2

LOGIN_REDIRECT_URL = '/'

MAX_ARTICLE_FILE_SIZE = 2 * 1024 * 1024
MAX_ARTICLE_PAGES = 3
