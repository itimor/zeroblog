# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts
import easyquotation as eq


def get_stocks(date):
    table = f'{db}_{level}'
    df = pd.read_sql_query(f'select * from {table}', con=engine)
    codes = ','.join(df['code'].to_list())
    if len(codes) > 0:
        df_a = ts_data.daily(ts_code=codes, start_date=date, end_date=date)
        df_a_columns = ['ts_code', 'open', 'high', 'low', 'change']
        new_df = pd.merge(df, df_a[df_a_columns], how='left', left_on=['code'], right_on=['ts_code'])
        new_df.loc[new_df.close > new_df.open, 'ogc'] = '1'
        columns = ['code', 'name', 'close', 'return', 'master', 'super', 'big', 'mid', 'small', 'open', 'high', 'low',
                   'change', 'ogc']
        df_b = new_df[columns]
        print(df_b[:5])
        df_b.to_sql(f'{db}_{level}', con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    db = 'bbb'
    level = 7
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    # 获得当天
    dd = datetime.now()
    start_date = dd - timedelta(days=10)
    end_date = dd - timedelta(days=1)
    cur_t = dd.strftime(t_format)
    if dd.hour > 15:
        # ts初始化
        ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
        df = ts_data.trade_cal(exchange='', start_date=start_date.strftime(d_format),
                               end_date=end_date.strftime(d_format), is_open='1')
        last_d = df.tail(1)['cal_date'].to_list()[0]
        last_day = datetime.strptime(last_d, d_format)
        cur_date = last_day.strftime(date_format)
        print(cur_date)
        # eq初始化
        eq_data = eq.use('sina')
        # 创建连接引擎
        engine = create_engine(f'sqlite:///{cur_date}/{db}.db', echo=False, encoding='utf-8')
        get_stocks(last_d)

