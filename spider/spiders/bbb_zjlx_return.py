# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票，并发送到tg频道

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts
from bbb_zjlx import get_stocks as new_stocks


def get_stocks():
    dfs = new_stocks()
    print(dfs[:5])
    for zjlx in tables:
        table = f'{db}_{zjlx}'
        print(table)
        try:
            df = pd.read_sql_query(f'select * from {table}', con=engine)
            if len(df) == 0:
                continue
        except Exception as e:
            continue
        super_list = []
        for code in df['code']:
            print(code)
            super_list.append(dfs[dfs['code'] == code]['super'])
            # df[df['code'] == code]['big_0'] = dfs[dfs['code'] == code]['big']
            # df[df['code'] == code]['master_0'] = dfs[dfs['code'] == code]['master']
            # df[df['code'] == code]['mid_0'] = dfs[dfs['code'] == code]['mid']
            # df[df['code'] == code]['small_0'] = dfs[dfs['code'] == code]['small']
        df['super_1'] = super_list
        df['close'].name
        print(df[:5])
        # df['return_1'] = (df['close_1'] - df['close_0']) / df['close_0'] * 100
        df.round({'return_1': 2}).to_sql(table, con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    db = 'bbb'
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    # 获得当天
    dd = datetime.now()
    cur_date = dd.strftime(date_format)
    # ts初始化
    # ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
    # d = dd.strftime(d_format)
    # df = ts_data.trade_cal(exchange='', start_date=d, end_date=d, is_open='1')
    # print(df)
    if dd.hour > 5:
        tables = [datetime.strftime(x, t_format) for x in
                  pd.date_range(f'{cur_date} 13:30', f'{cur_date} 15:00:00', freq='30min')]
        # 创建连接引擎
        engine = create_engine(f'sqlite:///{cur_date}/{db}.db', echo=False, encoding='utf-8')
        get_stocks()
