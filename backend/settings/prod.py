from .common import *
import os
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-620w%=z3%fmo5vl=)bof1ot6+otsvtids=1sh0#vxt0i)+)uv2' )

DEBUG = False

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'eleana-abra-test-message-app.herokuapp.com' ]

STATIC_HOST = "https://d4663kmspf1sqa.cloudfront.net" 
#STATIC_URL = STATIC_HOST + "/static/"

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}