# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票，并发送到tg频道

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts

tables = ['zjlx_1', 'zjlx_3', 'zjlx_5', 'zjlx_10']


def get_stocks(d1, d2):
    code_info_dict = dict()
    for table in tables:
        df = pd.read_sql_query(f'select * from {table}', con=engine)
        if len(df) == 0:
            return
        close_1 = []
        for code in df['code']:
            if code in code_info_dict:
                close_1.append(code_info_dict[code])
                continue
            print(code)
            code_info = ts_data.daily(ts_code=code, start_date=d1, end_date=d2)
            if len(code_info) == 1:
                code_info_dict[code] = code_info.iat[0, 5]
                close_1.append(code_info.iat[0, 5])

        df['close_1'] = close_1
        print(df[:5])
        df['return_1'] = (df['close_1'] - df['close_0']) / df['close_0'] * 100
        df.round({'return_1': 2}).to_sql(table, con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    # 获得当天
    dd = datetime.now()
    # 获取股票交易日期
    start_date = (dd - timedelta(11)).strftime(d_format)
    end_date = dd.strftime(d_format)
    # ts初始化
    ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
    # df = ts_data.trade_cal(exchange='', start_date=start_date, end_date=end_date, is_open='1')
    # df_a = df.sort_values(by=['cal_date'], ascending=[False])
    # d = 1
    # date = datetime.strptime(df_a.iat[d, 1], d_format).strftime(date_format)
    # d1 = df_a.iat[d - 1, 1]
    # d2 = df_a.iat[0, 1]
    date = '2020-12-31'
    d1 = '20210104'
    d2 = '20210104'
    print(date, d1, d2)
    # 创建连接引擎
    engine = create_engine(f'sqlite:///{date}/aaa.db', echo=False, encoding='utf-8')
    get_stocks(d1, d2)
