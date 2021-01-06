# -*- coding: utf-8 -*-
# author: itimor
# 统计资金流向，找出涨幅的资金分布区

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts

df_rank = {'v1': 'return_1 >= 9',
           'v2': 'return_1 >= 8 and return_1 < 9',
           'v3': 'return_1 >= 7 and return_1 < 8',
           'v4': 'return_1 >= 6 and return_1 < 7',
           'v5': 'return_1 >= 7 and return_1 < 6',
           'v6': 'return_1 >= 3 and return_1 < 5',
           'v7': 'return_1 >= 0 and return_1 < 3',
           }

area_level = [i for i in range(31)]
label_level = [i for i in range(30)]
tactics = ['master', 'super', 'big']


def get_stocks(date):
    d1 = pd.Series([date] * len(label_level))
    l1 = pd.Series(label_level)
    df = pd.DataFrame({
        'date': d1,
        'l1': l1,
    })
    for zjlx in tables:
        table = f'{db}_{zjlx}'
        for tactic in tactics:
            for rank_level, v in df_rank.items():
                try:
                    df_a = pd.read_sql_query(f'select {tactic} from {table} where {v}', con=engine)
                except:
                    continue
                print(f'{table} {tactic} {rank_level}')
                if len(df_a) > 0:
                    a = df_a[tactic].to_list()
                else:
                    a = [0] * len(label_level)
                cut = pd.cut(a, area_level, labels=label_level)
                b = cut.value_counts().sort_index().to_list()
                df[rank_level] = b
                df[rank_level] = df[rank_level] / df[rank_level].sum()
                df = df.replace(np.nan, 0)
                df.to_sql(f'{table}_{tactic}', con=engine, index=False, if_exists='replace')


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
    if len(df) > 0 and dd.hour > 19:
        tables = [datetime.strftime(x, t_format) for x in
                  pd.date_range(f'{cur_date} 09:50', f'{cur_date} 11:20:00', freq='10min')]
        # 创建连接引擎
        engine = create_engine(f'sqlite:///{cur_date}/{db}.db', echo=False, encoding='utf-8')
        get_stocks(cur_date)
