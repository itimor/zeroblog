# -*- coding: utf-8 -*-
# author: itimor
# 统计资金流向，找出涨幅的资金分布区

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts

# ts初始化
ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')

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
    df_rank['ranks_' + str(i)] = {'_v1': 'return_1 >= 9',
                                  '_v2': 'return_1 >= 8 and return_1 < 9',
                                  '_v3': 'return_1 >= 7 and return_1 < 8',
                                  '_v4': 'return_1 >= 6 and return_1 < 7',
                                  '_v5': 'return_1 >= 7 and return_1 < 6',
                                  '_v6': 'return_1 >= 3 and return_1 < 5',
                                  '_v7': 'return_1 >= 0 and return_1 < 3',
                                  }
df_rank['ranks_test'] = {'_v1': 'return_1 >= 0',
                         '_v2': 'return_1 < 0'}

area_level = [0, 10, 20, 30, 40, 50, 60, 100]
label_level = ['0-10', '10-20', '20-30', '30-40', '40-50', '50-60', '60-100']
tactics = ['master', 'super', 'big']


def get_stocks(date):
    d1 = pd.Series([date] * len(tactics) * len(label_level))
    s = pd.Series([date] * len(tactics) * len(label_level))
    df_a = pd.DataFrame({
        'date': d1,
        'tactic': np.nan,
        'level': np.nan,
        'v1': np.nan,
        'v2': np.nan,
        'v3': np.nan,
        'v4': np.nan,
        'v5': np.nan,
        'v6': np.nan,
        'v7': np.nan,
    })
    for rank_name, k in df_rank.items():
        for rank_level, v in k.items():
            print(f'{rank_name} {rank_level} {v}')
            df = pd.read_sql_query(f'select * from zjlx_data where create_date="{date}" and {v}', con=engine)
            if len(df) == 0:
                continue
            for tactic in tactics:
                cut = pd.cut(df[tactic], area_level, labels=label_level)
                print(cut.value_counts())


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
