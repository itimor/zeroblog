# -*- coding: utf-8 -*-
# author: itimor

APP_ENV = 'dev'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '64318ob@vbou7h50)b0a_pfda4d$bw2nhl4h*m$qo0_e_fxw=658!z*x'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# mysql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'zerostock',
        'USER': 'root',
        'PASSWORD': 'momo520',
        'HOST': 'localhost',
        'OPTIONS': {
            "init_command": "SET foreign_key_checks=0;",
        }
    }
}