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
engine = create_engine('sqlite:///new_zjlx.db', echo=False, encoding='utf-8')

zjlx_list = {
    'zjlx_1': {
        'columns': ['close_0', 'return_0', 'pre_code', 'name', 'super', 'big', 'mid', 'small', 'master'],
        'url': 'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=3000&po=1&np=1&ut=b2884a393a59ad64002292a3e90d46a5&fltt=2&invt=2&fid0=f4001&fid=f62&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&stat=1&fields=f12,f14,f2,f3,f184,f69,f75,f81,f87&rt=53658803&cb=jQuery18307545864640209479_1609764020312&_=1609764093954'
    }, 'zjlx_3': {
        'columns': ['close_0', 'pre_code', 'name', 'return_0', 'super', 'big', 'mid', 'small', 'master'],
        'url': 'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=3000&po=1&np=1&ut=b2884a393a59ad64002292a3e90d46a5&fltt=2&invt=2&fid0=f4001&fid=f267&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&stat=3&fields=f12,f14,f2,f127,f268,f270,f272,f274,f276&rt=53658808&cb=jQuery18307545864640209479_1609764020312&_=1609764263473'
    }, 'zjlx_5': {
        'columns': ['close_0', 'pre_code', 'name', 'return_0', 'super', 'big', 'mid', 'small', 'master'],
        'url': 'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=3000&po=1&np=1&ut=b2884a393a59ad64002292a3e90d46a5&fltt=2&invt=2&fid0=f4001&fid=f164&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&stat=5&fields=f12,f14,f2,f109,f165,f167,f169,f171,f173&rt=53658810&cb=jQuery18307545864640209479_1609764020312&_=1609764300393'
    }, 'zjlx_10': {
        'columns': ['close_0', 'pre_code', 'name', 'return_0', 'super', 'big', 'mid', 'small', 'master'],
        'url': 'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz=3000&po=1&np=1&ut=b2884a393a59ad64002292a3e90d46a5&fltt=2&invt=2&fid0=f4001&fid=f174&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&stat=10&fields=f12,f14,f2,f160,f175,f177,f179,f181,f183&rt=53658810&cb=jQuery18307545864640209479_1609764020312&_=1609764321169'}
}


def get_stocks(info):
    r = requests.get(info['url'], headers=headers).text
    X = re.split('}}', r)[0]
    X = re.split('"diff":', X)[1]
    df = pd.read_json(X, orient='records')
    print(df[:5])
    df.columns = info['columns']
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
    # dfs = df[~ df['name'].str.contains('ST')]
    # last_dfs = dfs[~ dfs['code'].str.contains('^300|^688|^900')]
    return df


def main(date):
    t1 = int(time.time() * 1000)
    t2 = t1 - 31
    for name, info in zjlx_list.items():
        print(name)
        dfs = get_stocks(info)
        df = dfs.loc[
            (dfs["close_0"] < 50) &
            (dfs["mid"] < 0) &
            (dfs["small"] < 0)]
        df[['close_1']] = np.nan
        df[['return_1']] = np.nan
        print(df[:5])
        df.to_sql(f'{date}_{name}', con=engine, index=False, if_exists='replace')


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
        main(cur_date)

