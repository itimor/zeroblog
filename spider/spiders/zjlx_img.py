# -*- coding: utf-8 -*-
# author: itimor
# 统计资金流向，找出涨幅的资金分布区

from datetime import datetime, timedelta
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts
import matplotlib.pyplot as plt

# 创建连接引擎
engine = create_engine('sqlite:///zjlx.db', echo=False, encoding='utf-8')

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

colunms_name = ['date', 'l1', '最强王者', '至尊星耀', '永恒钻石', '尊贵铂金', '荣耀黄金', '秩序白银', '倔强青铜']


def get_stocks(date):
    # zjlx_ranks_1
    table = 'zjlx_ranks_1_master'
    df_zjlx_ranks_1_master = pd.read_sql_query(f'select * from {table} where date="{date}"', con=engine)
    df_zjlx_ranks_1_master.columns = colunms_name
    df_zjlx_ranks_1_master.plot(x='l1')
    # 图片标题
    plt.title(f'{table}')
    # x坐标轴文本
    plt.xlabel('资金流入占比')
    # y坐标轴文本
    plt.ylabel('涨幅占比')
    # 显示网格
    plt.grid(True)

    table = 'zjlx_ranks_1_super'
    df_zjlx_ranks_1_super = pd.read_sql_query(f'select * from {table} where date="{date}"', con=engine)
    df_zjlx_ranks_1_super.columns = colunms_name
    df_zjlx_ranks_1_super.plot(x='l1')
    # 图片标题
    plt.title(f'{table}')
    # x坐标轴文本
    plt.xlabel('资金流入占比')
    # y坐标轴文本
    plt.ylabel('涨幅占比')
    # 显示网格
    plt.grid(True)

    table = 'zjlx_ranks_1_big'
    df_zjlx_ranks_1_big = pd.read_sql_query(f'select * from {table} where date="{date}"', con=engine)
    df_zjlx_ranks_1_big.columns = colunms_name
    df_zjlx_ranks_1_big.plot(x='l1')
    # 图片标题
    plt.title(f'{table}')
    # x坐标轴文本
    plt.xlabel('资金流入占比')
    # y坐标轴文本
    plt.ylabel('涨幅占比')
    # 显示网格
    plt.grid(True)


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
    get_stocks(date)
    # 显示图形
    plt.show()

