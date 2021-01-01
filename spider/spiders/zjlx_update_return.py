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
df = ts_data.daily(ts_code='000001.SZ', start_date='20180718', end_date='20180718')
# print(df)
# print(df.iat[0, 6])

# es初始化
eq = es.use('sina')  # 新浪 ['sina'] 腾讯 ['tencent', 'qq']

# 创建连接引擎
engine = create_engine('sqlite:////Users/sha/data/zjlx/zjlx.db', echo=False, encoding='utf-8')


def get_stocks(table, date, d1, d2):
    df = pd.read_sql_query(f'select * from {table} where create_date="{date}"', con=engine)
    return_1 = []
    return_2 = []
    return_3 = []
    for code in df['code']:
        code_info = ts_data.daily(ts_code=code, start_date=d1, end_date=d2)
        print(code)
        if len(code_info) > 0:
            return_1.append(code_info.iat[2, 5])
            return_2.append(code_info.iat[1, 5])
            return_3.append(code_info.iat[0, 5])
        else:
            return_1.append(None)
            return_2.append(None)
            return_3.append(None)

    df['return_1'] = return_1
    df['return_2'] = return_2
    df['return_3'] = return_3
    print(df.head())
    df.to_sql(table, con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    table = 'zjlx_data'
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    date = '2020-12-27'
    dd = datetime.strptime(date, date_format)
    d1 = (dd + timedelta(1)).strftime(d_format)
    d2 = (dd + timedelta(3)).strftime(d_format)
    get_stocks(table, date, d1, d2)
