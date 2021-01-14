# -*- coding: utf-8 -*-
# author: itimor
# 东方财富沪深a股实时行情

from datetime import datetime, timedelta
from fake_useragent import UserAgent
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts
import re
import requests
import os

ua = UserAgent()
headers = {'User-Agent': ua.random}


def get_df(url):
    timestamp = datetime.timestamp(dd)
    t1 = int(timestamp * 1000)
    r = requests.get(url, headers=headers).text
    X = re.split('}}', r)[0]
    X = re.split('"diff":', X)[1]
    df_a = pd.read_json(X, orient='records')
    df = df_a[['f12', 'f14', 'f2', 'f3', 'f15', 'f16', 'f17', 'f7', 'f10']]
    df.columns = ['pre_code', 'name', 'close', 'return', 'high', 'low', 'open', 'amp', 'qr']  # 最后面振幅和量比
    return df


def get_stocks():
    num = 2000
    sh_url = f'http://62.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112406138402393308908_1610615965583&pn=1&pz={num}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1610615966013'
    sz_url = f'http://62.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112406138402393308908_1610615965583&pn=1&pz={num}&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:13,m:0+t:80&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1610615966015'
    df_sh = get_df(sh_url)
    df_sz = get_df(sz_url)
    df = df_sh.append(df_sz, ignore_index=True)
    df['code'] = str(df['pre_code'])
    s_codes = []
    for i in df['pre_code']:
        if len(str(i)) < 6:
            s = '0' * (6 - len(str(i))) + str(i)
        else:
            s = str(i)
        if s[0] == '6':
            s = s + '.SH'
        else:
            s = s + '.SZ'
        if len(s_codes) == 0:
            s_codes = [s]
        else:
            s_codes.append(s)
    df['code'] = s_codes
    df.drop(['pre_code'], axis=1, inplace=True)
    dfs = df[~ df['name'].str.contains('ST')]
    last_dfs = dfs[~ dfs['code'].str.contains('^300|^688|^900')]
    return last_dfs


def main():
    dfs = get_stocks()
    columns = ['code', 'name', 'close', 'return', 'high', 'low', 'open', 'amp', 'qr']
    df = dfs.loc[
        (dfs["close"] < 50) &
        (dfs["return"] > 0), columns]
    print(df)
    # df.to_sql(f'{db}', con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    db = 'bbb'
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    # 获得当天
    dd = datetime.now()
    cur_date = dd.strftime(date_format)
    cur_t = dd.strftime(t_format)
    if dd.hour > 15:
        # ts初始化
        ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
        df = ts_data.trade_cal(exchange='', start_date=dd.strftime(d_format), end_date=dd.strftime(d_format),
                               is_open='1')
        print(df)
        if not os.path.exists(cur_date):
            os.makedirs(cur_date)

        # 创建连接引擎
        engine = create_engine(f'sqlite:///{cur_date}/{db}.db', echo=False, encoding='utf-8')
        main()

