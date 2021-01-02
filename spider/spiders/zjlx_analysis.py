# -*- coding: utf-8 -*-
# author: itimor
# 统计资金流向，找出涨幅的资金分布区

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts

# ts初始化
# ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')

# 创建连接引擎
engine = create_engine('sqlite:///zjlx.db', echo=False, encoding='utf-8')

# 最强王者：9
# 至尊星耀：8 - 9
# 永恒钻石：7 - 8
# 尊贵铂金：6 - 7
# 荣耀黄金：5 - 6
# 秩序白银：3 - 5
# 倔强青铜：0 - 3
df_rank = dict()
for i in range(1, 4):
    df_rank['ranks_' + str(i)] = {'v1': 'return_1 >= 9',
                                  'v2': 'return_1 >= 8 and return_1 < 9',
                                  'v3': 'return_1 >= 7 and return_1 < 8',
                                  'v4': 'return_1 >= 6 and return_1 < 7',
                                  'v5': 'return_1 >= 7 and return_1 < 6',
                                  'v6': 'return_1 >= 3 and return_1 < 5',
                                  'v7': 'return_1 >= 0 and return_1 < 3',
                                  }

area_level = [0, 10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
label_level = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-70', '70-80', '80-90', '90-100']
tactics = ['master', 'super', 'big']


def get_stocks(date):
    d1 = pd.Series([date] * len(tactics) * len(label_level))
    t = list()
    for i in range(len(tactics)):
        t += [tactics[i]] * len(label_level)
    t1 = pd.Series(t)
    l1 = pd.Series(label_level * len(tactics))
    for rank_name, k in df_rank.items():
        df = pd.DataFrame({
            'date': d1,
            't1': t1,
            'l1': l1,
        })
        for rank_level, v in k.items():
            print(f'{rank_name} {rank_level} {v}')
            df_a = pd.read_sql_query(f'select * from zjlx_data where create_date="{date}" and {v}', con=engine)
            for tactic in tactics:
                cut = pd.cut(df_a[tactic], area_level, labels=label_level)
                a = cut.value_counts().sort_index().to_list()
                df.loc[(df.date == date) & (df.t1 == tactic), rank_level] = a
        df.to_sql('zjlx_analysis_' + str(rank_name), con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    # 获得当天
    dd = datetime.now()
    # 获取股票交易日期
    # start_date = (dd - timedelta(11)).strftime(d_format)
    # end_date = dd.strftime(d_format)
    # df = ts_data.trade_cal(exchange='', start_date=start_date, end_date=end_date, is_open='1')
    # date = datetime.strptime(df.iat[4, 1], d_format).strftime(date_format)
    date = '2020-12-31'
    print(date)
    get_stocks(date)

