# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票，并发送到tg频道

from datetime import datetime, timedelta
from fake_useragent import UserAgent
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts

ua = UserAgent()
headers = {'User-Agent': ua.random}

# ts初始化
ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
# df = ts_data.daily(ts_code='000001.SZ', start_date='20180718', end_date='20180718')
# print(df)
# print(df.iat[0, 6])

# 创建连接引擎
engine = create_engine('sqlite:///zjlx.db', echo=False, encoding='utf-8')


def get_stocks(table, date, d1, d2):
    df = pd.read_sql_query(f'select * from {table} where create_date="{date}"', con=engine)
    close_1 = []
    close_2 = []
    close_3 = []
    for code in df['code']:
        code_info = ts_data.daily(ts_code=code, start_date=d1, end_date=d2)
        print(code)
        if len(code_info) > 0:
            close_1.append(code_info.iat[2, 5])
            close_2.append(code_info.iat[1, 5])
            close_3.append(code_info.iat[0, 5])
        else:
            close_1.append(np.nan)
            close_2.append(np.nan)
            close_3.append(np.nan)

    for i in range(1, 4):
        df['close_' + str(i)] = eval('close_' + str(i))
        df['return_' + str(i)] = (df['close_' + str(i)] - df['close_0']) / df['close_0']

    df.round({'return_1': 2, 'return_2': 2, 'return_3': 2}).to_sql(table, con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    table = 'zjlx_data'
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    date = '2020-12-31'
    dd = datetime.strptime(date, date_format)
    # 获取股票交易日期
    start_date = (dd - timedelta(11)).strftime(d_format)
    end_date = (dd - timedelta(1)).strftime(d_format)
    df = ts_data.trade_cal(exchange='', start_date=start_date, end_date=end_date, is_open='1')
    print(df)
    d1 = df.iat[0, 1]
    d2 = df.iat[2, 1]
    get_stocks(table, date, d1, d2)

