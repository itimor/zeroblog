# -*- coding: utf-8 -*-
# author: itimor
# 东方财富沪深a股实时行情

from datetime import datetime, timedelta
from fake_useragent import UserAgent
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts
import requests
import re

ua = UserAgent()
headers = {'User-Agent': ua.random}


def get_stock(code):
    url = f'http://hq.sinajs.cn/list={code}'
    r = requests.get(url, headers=headers).text
    X = re.split('";', r)[0]
    X = re.split('="', X)[1]
    print(X)


if __name__ == '__main__':
    code = 'sz002463'
    get_stock(code)

