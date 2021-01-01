# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票，并发送到tg频道

from datetime import datetime, timedelta
from fake_useragent import UserAgent
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts
import easyquotation as es
import time
import re
import requests

ua = UserAgent()
headers = {'User-Agent': ua.random}

# ts初始化
ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')

# es初始化
eq = es.use('sina')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

# 创建连接引擎
engine = create_engine('sqlite:////Users/sha/data/zjlx/zjlx.db', echo=False, encoding='utf-8')


def get_stocks(table, d0, d1, d2):
    df = pd.read_sql_query(f'select * from {table} where create_date="{d0}"', con=engine)
    return_1 = []
    return_2 = []
    for code in df['code']:
        print(code)
        code_info = ts_data.daily(ts_code=code, start_date=d1, end_date=d2)
        return_1.append(code_info['close'])

    df['return_2'] = return_1
    print(df.head())
    df.to_sql(table, con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    table = 'zjlx_data'
    date = '2020-12-30'
    get_stocks(table, date)
