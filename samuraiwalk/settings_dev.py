from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = True

ALLOWED_HOSTS = []

# ロギング設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'logger': {
        'django': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
        'account': {
            'handler': ['console'],
            'level': 'DEBUG',
        },
    },
    'handler': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'dev'
        },
    },
    'formatter': {
        'dev': {
            'format':
            '\t'.join([
                '%(astime)s', '[%(levelname)s]',
                '%(pathneme)s(Line:%(lineno)d)', '%(message)s'
            ])
        },
    }
}
#-------------------
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

MEDIA_ROOT = os.path.join(BASE_DIR,'media')