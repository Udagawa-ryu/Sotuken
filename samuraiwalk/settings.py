from .settings_common import *

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = False

ALLOWED_HOSTS = [os.environ.get('ALLOWED_HOSTS')]

STATIC_ROOT = 'usr/share/nginx/html/static'
MEDIA_ROOT = 'usr/share/nginxhtml/media'

# ロギング設定
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'logger': {
        'django': {
            'handlers': ['file'],
            'level': 'INFO',
        },
        'account': {
            'handler': ['file'],
            'level': 'INFO',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'formatter': 'prod',
            'when': 'D',
            'interval': 1,
            'backupCount':7,
        },
    },
    'formatters': {
        'prod': {
            'format':
            '\t'.join([
                '%(astime)s', '[%(levelname)s]',
                '%(pathneme)s(Line:%(lineno)d)', '%(message)s'
            ])
        },
    }
}
#-------------------
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/home/app_admin/log'
MEDIA_ROOT = os.path.join(BASE_DIR,'media')