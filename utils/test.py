# -*- coding: utf-8 -*-
# author: itimor
# description: 递归解析json

import re

a = ['实力游资买入，成功率33.44%', '一个机构买入，成功率55.44%']

for i in a:
    b = re.findall('(实力游资|机构)(买入|卖出)，成功率(\d+.\d+)%', i)[0]
    if float(b[2]) >= 45:
        print(i)
