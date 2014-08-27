import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
SECRET_KEY = 'dk)s2e105ct2t7@vh%awj(qk=@%!54^mp4d(is-=9yc+u&+r)n'
DEBUG = True
TEMPLATE_DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'celery',
    'kombu.transport.django',
    'dj_test_app',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'dj_test_app.urls'
WSGI_APPLICATION = 'dj_test_app.wsgi.application'
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True
STATIC_URL = '/static/'

# -- Celery Config -- #
import djcelery
djcelery.setup_loader()
CELERY_RESULT_BACKEND = 'djcelery.backends.database:DatabaseBackend'
CELERY_TIMEZONE = 'UTC'
CELERY_ACCEPT_CONTENT = ['json','pickle','yaml']
BROKER_URL = 'amqp://rmq_user:abc123@localhost:5672/rmq_host'
CELERY_DEFAULT_QUEUE = 'default'

