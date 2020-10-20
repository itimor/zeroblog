# -*- coding: utf-8 -*-
# author: itimor

import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'blog.settings'
django.setup()

from myblog.models import *
from spider.models import *
