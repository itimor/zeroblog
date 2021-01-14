# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票

from datetime import datetime, timedelta
from fake_useragent import UserAgent
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts
import requests
import re
import json

ua = UserAgent()
headers = {'User-Agent': ua.random}


def get_stocks(codes):
    dfs = []
    for pre_code in codes:
        print(pre_code)
        c = pre_code.split('.')
        code = f'{c[1].lower()}{c[0]}'
        url = f'http://hq.sinajs.cn/list={code}'
        r = requests.get(url, headers=headers).text
        X = re.split('";', r)[0]
        X = re.split('="', X)[1]
        d = X.split(',')
        d_data = {
            'code': pre_code,
            'open': d[1],
            'now': d[3],
            'high': d[4],
            'low': d[5],
            'change': float(d[3]) - float(d[2]),
            'ogc': float(d[1]) - float(d[2]),
        }
        dfs.append(d_data)
    dfs_json = json.dumps(dfs)
    df_a = pd.read_json(dfs_json, orient='records')
    return df_a


def main():
    table = f'{db}_x'
    df = pd.read_sql_query(f'select * from {table}', con=engine)
    df_a = get_stocks(df['code'].to_list())
    if len(df_a) > 0:
        new_df = pd.merge(df, df_a, how='inner', left_on=['code'], right_on=['code'])
        columns = ['code', 'name', 'close', 'return', 'master', 'super', 'big', 'mid', 'small', 'open', 'now', 'high',
                   'low', 'change', 'ogc']
        df_b = new_df[columns]
        print(df_b[:5])
        df_b.to_sql(table, con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    db = 'bbb'
    level = 5
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    # 获得当天
    dd = datetime.now()
    cur_date = dd.strftime(date_format)
    cur_d = dd.strftime(d_format)
    cur_t = dd.strftime(t_format)
    if dd.hour > 15:
        # ts初始化
        ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
        df = ts_data.trade_cal(exchange='', start_date=cur_d, end_date=cur_d, is_open='1')
        print(df)
        # 创建连接引擎
        engine = create_engine(f'sqlite:///{cur_date}/{db}.db', echo=False, encoding='utf-8')
        main()

