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

area_level = [i for i in range(101)]
label_level = [i for i in range(100)]
tactics = ['master', 'super', 'big']


def get_stocks(date):
    d1 = pd.Series([date] * len(label_level))
    l1 = pd.Series(label_level)
    df = pd.DataFrame({
        'date': d1,
        'l1': l1,
    })
    for i in [1, 3, 5, 10]:
        table = f'zjlx_{i}'
        print(table)
        for tactic in tactics:
            for rank_level, v in df_rank.items():
                print(f'{tactic} {rank_level}')
                df_a = pd.read_sql_query(f'select {tactic} from {table} where {v}', con=engine)
                if len(df_a) > 0:
                    a = df_a[tactic].to_list()
                else:
                    a = [0] * len(label_level)
                cut = pd.cut(a, area_level, labels=label_level)
                b = cut.value_counts().sort_index().to_list()
                df.loc[df.date == date, rank_level] = b
                df[rank_level] = df[rank_level] / df[rank_level].sum()
                df = df.replace(np.nan, 0)
                df.to_sql(tactic, con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    # 获得当天
    dd = datetime.now()
    # 获取股票交易日期
    start_date = (dd - timedelta(11)).strftime(d_format)
    end_date = dd.strftime(d_format)
    # ts初始化
    # ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
    # df = ts_data.trade_cal(exchange='', start_date=start_date, end_date=end_date, is_open='1')
    # df_a = df.sort_values(by=['cal_date'], ascending=[False])
    # d = 1
    # date = datetime.strptime(df_a.iat[d, 1], d_format).strftime(date_format)
    date = '2020-12-31'
    print(date)
    # 创建连接引擎
    engine = create_engine(f'sqlite:///{date}/aaa.db', echo=False, encoding='utf-8')
    get_stocks(date)
