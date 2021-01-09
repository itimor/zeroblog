# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票，并发送到tg频道

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import numpy as np


def get_stocks():
    df_1600 = pd.read_sql_query(f'select code,name,close,return from {db}_1600', con=engine)
    last_df = pd.DataFrame()
    last_time = ''
    for zjlx in t_list:
        table = f'{db}_{zjlx}'
        print(table)
        try:
            df = pd.read_sql_query(f'select * from {table}', con=engine)
            if len(df) == 0:
                continue
        except Exception as e:
            continue
        if len(last_df) == 0:
            last_df = df
            last_time = zjlx
            continue
        else:
            df_a = pd.merge(last_df, df, on=['code', 'name'], suffixes=['_0', '_1'])
            columns = ['return', 'master', 'super', 'big', 'mid', 'small']
            for column in columns:
                df_a[column + '_x'] = df_a[column + '_1'] - df_a[column + '_0']
            print(df_a[:5])
            columns = ['code', 'name', 'close_x', 'return_x', 'master_x', 'super_x', 'big_x', 'mid_x', 'small_x']
            new_df = df_a.loc[(df_a["return_x"] > 0), columns]
            new_df.merge(df_1600, on=['code', 'name'])
            new_table = f'{db}_{last_time}-{zjlx}'
            new_df.to_sql(new_table, con=engine, index=False, if_exists='replace')
            last_df = df
            last_time = zjlx


if __name__ == '__main__':
    db = 'aaa'
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    # 获得当天
    dd = datetime.now()
    cur_date = dd.strftime(date_format)
    t_list = [datetime.strftime(x, t_format) for x in
              pd.date_range(f'{cur_date} 10:00', f'{cur_date} 11:30:00', freq='10min')]
    t_list_pm = [datetime.strftime(x, t_format) for x in
                 pd.date_range(f'{cur_date} 13:10', f'{cur_date} 14:50:00', freq='10min')]
    t_list.extend(t_list_pm)
    cur_t = dd.strftime(t_format)
    if dd.hour > 15:
        # 创建连接引擎
        engine = create_engine(f'sqlite:///{cur_date}/{db}.db', echo=False, encoding='utf-8')
        get_stocks()

