# -*- coding: utf-8 -*-
# author: itimor

import platform
from .base import *

os_type = platform.system()

if os_type == 'Windows':
    print('进入 windows ')
    from .win import *
else:
    print('进入 unix ')
    from .mac import *
