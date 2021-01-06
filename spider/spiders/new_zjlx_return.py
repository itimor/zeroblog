# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票，并发送到tg频道

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts


def get_stocks(d1, d2):
    code_info_dict = dict()
    for table in tables:
        try:
            df = pd.read_sql_query(f'select * from {db}_{table}', con=engine)
            if len(df) == 0:
                continue
        except Exception as e:
            continue
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
            else:
                close_1.append(np.nan)

        df['close_1'] = close_1
        print(df[:5])
        df['return_1'] = (df['close_1'] - df['close_0']) / df['close_0'] * 100
        df.round({'return_1': 2}).to_sql(table, con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    db = 'aaa'
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    # 获得当天
    dd = datetime.now()
    cur_date = dd.strftime(date_format)
    # ts初始化
    ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
    d = dd.strftime(d_format)
    df = ts_data.trade_cal(exchange='', start_date=d, end_date=d, is_open='1')
    print(df)
    if len(df) > 0:
        tables = [datetime.strftime(x, t_format) for x in
                  pd.date_range(f'{cur_date} 09:50', f'{cur_date} 11:20:00', freq='10min')]
        # 创建连接引擎
        engine = create_engine(f'sqlite:///{cur_date}/{db}.db', echo=False, encoding='utf-8')
        get_stocks(d, d)
