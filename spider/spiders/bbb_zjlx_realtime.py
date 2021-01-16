# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票

from datetime import datetime, timedelta
from telegram import Bot, ParseMode
from fake_useragent import UserAgent
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import tushare as ts
import requests
import re
import json

ua = UserAgent()
headers = {'User-Agent': ua.random}


def get_stocks(codes):
    dfs = []
    for pre_code in codes:
        print(pre_code)
        c = pre_code.split('.')
        code = f'{c[1].lower()}{c[0]}'
        url = f'http://hq.sinajs.cn/list={code}'
        r = requests.get(url, headers=headers).text
        X = re.split('";', r)[0]
        X = re.split('="', X)[1]
        d = X.split(',')
        d_data = {
            'code': pre_code,
            'open': d[1],
            'now': d[3],
            'high': d[4],
            'low': d[5],
            'change': (float(d[3]) - float(d[1])) / float(d[1]) * 100,
            'ogc': (float(d[1]) - float(d[2])) / float(d[2]) * 100,
        }
        dfs.append(d_data)
    dfs_json = json.dumps(dfs)
    df_a = pd.read_json(dfs_json, orient='records')
    return df_a


def send_tg(date, msg, chat_id):
    token = '723532221:AAH8SSfM7SfTe4HmhV72QdLbOUW3akphUL8'
    bot = Bot(token=token)
    chat_id = chat_id
    text = '%s 昨日涨幅>5今天低开前十\n' % date + msg
    bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)


def main(date):
    table = f'x_{date}'
    df = pd.read_sql_query(f'select * from {table}', con=engine)
    dfs = get_stocks(df['code'].to_list())
    if len(dfs) > 0:
        new_df = pd.merge(df, dfs, how='inner', left_on=['code'], right_on=['code'])
        columns = ['code', 'name', 'close', 'open', 'now', 'change', 'ogc']
        # 发送tg
        if tg:
            df_a = new_df.loc[
                # (new_df["ogc"] < -5) &
                (new_df["change"] < 5)
                , columns].sort_values(by=['ogc', 'change'], ascending=True)
            print(df_a.head())
            if len(df_a) > 0:
                last_df = df_a.head().round({'change': 2, 'ogc': 2}).to_string(header=None)
                chat_id = "@hollystock"
                send_tg(date, last_df, chat_id)
            df_b = new_df.loc[
                (new_df["return"] < 6) &
                (new_df["return"] > 0) &
                # (new_df["ogc"] < -5) &
                (new_df["change"] < 5)
                , columns].sort_values(by=['ogc', 'change'], ascending=False)
            print(df_b.head())
            if len(df_b) > 0:
                last_df = df_b.head().round({'change': 2, 'ogc': 2}).to_string(header=None)
                chat_id = "@timorstock"
                send_tg(date, last_df, chat_id)
        else:
            df_a = new_df.sort_values(by=['ogc', 'change'], ascending=True)
            print(df_a.head())
            df_a.to_sql(table, con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    db = 'bbb'
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    # 获得当天
    dd = datetime.now()
    start_date = dd - timedelta(days=10)
    end_date = dd - timedelta(days=1)
    cur_date = dd.strftime(date_format)
    cur_t = dd.strftime(t_format)
    t_list = [datetime.strftime(x, t_format) for x in pd.date_range(f'{cur_date} 09:16', f'{cur_date} 09:30:00', freq='6min')]
    if cur_t in t_list:
        tg = True
    else:
        tg = False
    if dd.hour > 9:
        # ts初始化
        ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
        df = ts_data.trade_cal(exchange='', start_date=start_date.strftime(d_format),
                               end_date=end_date.strftime(d_format), is_open='1')
        last_d = df.tail(1)['cal_date'].to_list()[0]
        # last_d = "20210115"
        last_day = datetime.strptime(last_d, d_format)
        last_date = last_day.strftime(date_format)
        # 创建连接引擎
        engine = create_engine(f'sqlite:///{last_date}/{db}.db', echo=False, encoding='utf-8')
        main(last_d)

