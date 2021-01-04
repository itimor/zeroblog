# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票，并发送到tg频道

from datetime import datetime, timedelta
from fake_useragent import UserAgent
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts
import time
import re
import requests

ua = UserAgent()
headers = {'User-Agent': ua.random}

# ts初始化
ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')

# 创建连接引擎
engine = create_engine('sqlite:///zjlx.db', echo=False, encoding='utf-8')


def get_stocks():
    t1 = int(time.time() * 1000)
    t2 = t1 - 31
    URL_stocks_infos = f'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=2000&po=1&np=1&ut=b2884a393a59ad64002292a3e90d46a5&fltt=2&invt=2&fid0=f4001&fid=f69&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&stat=1&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124&rt=53647283&cb=jQuery18307520567343556515_{t1}&_={t2}'
    r = requests.get(URL_stocks_infos, headers=headers).text
    X = re.split('}}', r)[0]
    X = re.split('"diff":', X)[1]
    df = pd.read_json(X, orient='records')
    if (len(df) != 0):
        df2 = df[['f124', 'f2', 'f3', 'f12', 'f14', 'f69', 'f75', 'f81', 'f87', 'f184']]
        colunms_name = ['close_0', 'return_0', 'pre_code', 'name', 'super', 'big', 'mid', 'small', 'master']
        df2 = df2.rename(
            columns={'f124': 'update_time', 'f12': colunms_name[2], 'f14': colunms_name[3], 'f2': colunms_name[0],
                     'f3': colunms_name[1], 'f69': colunms_name[4], 'f75': colunms_name[5], 'f81': colunms_name[6],
                     'f87': colunms_name[7], 'f184': colunms_name[8]})
        df2['code'] = str(df2['pre_code'])
        s_codes = []
        for i in df2['pre_code']:
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
        df2['code'] = s_codes
        # 排除st和300、688开头的股票
        dfs = df2[~ df2['name'].str.contains('ST')]
        last_dfs = dfs[~ dfs['code'].str.contains('^300|^688|^900')]
    return last_dfs


def main():
    dfs = get_stocks()
    display_name = ['update_time', 'code', 'name', 'super', 'big', 'mid', 'small', 'master', 'close_0', 'return_0']
    df = dfs.loc[
        (dfs["close_0"] < 50) &
        (dfs["super"] > 1) &
        (dfs["master"] > 1) &
        (dfs["big"] > 1) &
        (dfs["mid"] < 0) &
        (dfs["small"] < 0), display_name]
    df['update_time'] = pd.to_datetime(df['update_time'], unit='s')
    df['date'] = df['update_time'].dt.strftime(date_format)
    print(df[:5])
    df.to_sql('zjlx_data', con=engine, index=False, if_exists='append')


if __name__ == '__main__':
    t = 10
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    # 获得当天
    dd = datetime.now()
    if dd.hour > t:
        date = dd
    else:
        date = (dd - timedelta(1))
    df = ts_data.trade_cal(exchange='', start_date=date.strftime(d_format), end_date=date.strftime(d_format),
                           is_open='1')
    print(df)
    cur_date = date.strftime(date_format)
    if len(df) > 0:
        main()
