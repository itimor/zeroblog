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
            'change': float(d[3]) - float(d[2]),
            'ogc': float(d[1]) - float(d[2]),
        }
        dfs.append(d_data)
    dfs_json = json.dumps(dfs)
    df_a = pd.read_json(dfs_json, orient='records')
    return df_a


def send_tg(date, msg, chat_id):
    token = '723532221:AAH8SSfM7SfTe4HmhV72QdLbOUW3akphUL8'
    bot = Bot(token=token)
    chat_id = chat_id
    text = '%s 昨日大涨今天低开前十\n' % date + msg
    bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)


def main(date):
    table = f'{db}_x'
    df = pd.read_sql_query(f'select * from {table}', con=engine)
    df_a = get_stocks(df['code'].to_list())
    if len(df_a) > 0:
        new_df = pd.merge(df, df_a, how='inner', left_on=['code'], right_on=['code'])
        columns = ['code', 'name', 'close', 'return', 'open', 'now', 'ogc']
        df_b = new_df[columns].sort_values(by=['ogc'], ascending=True)
        print(df_b.head())
        last_df = df_b[:10].round({'ogc': 2}).to_string(header=None)
        # 发送tg
        if len(last_df) > 0:
            chat_id = "@hollystock"
            send_tg(date, last_df, chat_id)
        # df_b.to_sql(table, con=engine, index=False, if_exists='replace')


if __name__ == '__main__':
    db = 'bbb'
    level = 5
    date_format = '%Y-%m-%d'
    d_format = '%Y%m%d'
    t_format = '%H%M'
    # 获得当天
    dd = datetime.now()
    start_date = dd - timedelta(days=10)
    end_date = dd - timedelta(days=1)
    cur_date = dd.strftime(date_format)
    cur_t = dd.strftime(t_format)
    if dd.hour > 9:
        # ts初始化
        ts_data = ts.pro_api('d256364e28603e69dc6362aefb8eab76613b704035ee97b555ac79ab')
        df = ts_data.trade_cal(exchange='', start_date=start_date.strftime(d_format),
                               end_date=end_date.strftime(d_format), is_open='1')
        last_d = df.tail(1)['cal_date'].to_list()[0]
        last_day = datetime.strptime(last_d, d_format)
        last_date = last_day.strftime(date_format)
        # last_date = "2021-01-14"
        # 创建连接引擎
        engine = create_engine(f'sqlite:///{last_date}/{db}.db', echo=False, encoding='utf-8')
        main(cur_date)

