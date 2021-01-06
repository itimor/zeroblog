# -*- coding: utf-8 -*-
# author: itimor
# 统计资金流向，找出涨幅的资金分布区

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt

colunms_name = ['date', 'l1', 'v1', 'v2', 'v3', 'v4', 'v5', 'v6', 'v7']
tactics = ['master', 'super', 'big']


# zjlx_1  big 4-10  super 3 7  master 3 - 11
# zjlx_3  big 11-15  super 11 13 master 0 3
# zjlx_5  big 2 8  super 2 7  master 0 3
# SELECT * FROM zjlx_1  WHERE big > 4 AND big < 10 AND super > 3 AND super < 7 AND master  > 3 AND master < 11 ORDER by return_0;

def get_stocks():
    for zjlx in tables:
        for tactic in tactics:
            table = f'{zjlx}_{tactic}'
            df_zjlx_ranks_1_master = pd.read_sql_query(f'select * from {table}', con=engine)
            df_zjlx_ranks_1_master.columns = colunms_name
            df_zjlx_ranks_1_master.plot(x='l1')
            # 图片标题
            plt.title(table)
            # x坐标轴文本
            plt.xlabel('资金流入占比')
            # y坐标轴文本
            plt.ylabel('涨幅占比')
            # 显示网格
            plt.grid(True)


if __name__ == '__main__':
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
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
    date = '2021-01-06'
    print(date)
    tables = [datetime.strftime(x, t_format) for x in
              pd.date_range(f'{date} 09:50', f'{date} 11:20:00', freq='10min')]
    # 创建连接引擎
    engine = create_engine(f'sqlite:///{date}/aaa.db', echo=False, encoding='utf-8')
    get_stocks()
    # 显示图形
    plt.show()

