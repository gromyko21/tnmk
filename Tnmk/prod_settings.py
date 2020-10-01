import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SECRET_KEY = '@(^3%+6!stp#34534jgfk+@$u0#sr=^^vi%^s)2+d!!t_#*asisadfsdg$se2(43='

DEBUG = False

ALLOWED_HOSTS = ['ss.tnmk.ru']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'tnmk',
        'USER': 'tnmk',
        'PASSWORD': 'P9m3A1e7',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '3306',
    }
}

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
