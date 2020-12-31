# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票，并发送到tg频道

from datetime import datetime, timedelta
from telegram import Bot, ParseMode
from fake_useragent import UserAgent
from sqlalchemy import create_engine
import pandas as pd
import numpy as np
import time
import re
import requests

ua = UserAgent()

headers = {'User-Agent': ua.random}
engine = create_engine('sqlite:////Users/sha/data/zjlx/zjlx.db', echo=False)


def daterange(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.strptime, datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + timedelta(i), format) for i in range(0, days + 1, step)]


def get_stocks(num):
    dfs = pd.DataFrame()
    URL_stocks_infos = f'http://push2.eastmoney.com/api/qt/clist/get?pn=1&pz={num}&po=1&np=1&ut=b2884a393a59ad64002292a3e90d46a5&fltt=2&invt=2&fid0=f4001&fid=f69&fs=m:0+t:6+f:!2,m:0+t:13+f:!2,m:0+t:80+f:!2,m:1+t:2+f:!2,m:1+t:23+f:!2,m:0+t:7+f:!2,m:1+t:3+f:!2&stat=1&fields=f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124&rt=53647283&cb=jQuery18307520567343556515_{t1}&_={t2}'
    r = requests.get(URL_stocks_infos, headers=headers).text
    X = re.split('}}', r)[0]
    X = re.split('"diff":', X)[1]
    df = pd.read_json(X, orient='records')
    if (len(df) != 0):
        df2 = df[['f2', 'f3', 'f12', 'f14', 'f69', 'f75', 'f81', 'f87', 'f184']]
        colunms_name = ['Close', 'Radio', 'Code', 'Name', 'Super', 'Big', 'Mid', 'Small', 'Master']
        df2 = df2.rename(
            columns={'Tdate': 'Date', 'f12': colunms_name[2], 'f14': colunms_name[3], 'f2': colunms_name[0],
                     'f3': colunms_name[1], 'f69': colunms_name[4], 'f75': colunms_name[5], 'f81': colunms_name[6],
                     'f87': colunms_name[7], 'f184': colunms_name[8]})
        df2['Wind_Code'] = str(df2['Code'])
        s_codes = []
        for i in df2['Code']:
            if len(str(i)) < 6:
                s = '0' * (6 - len(str(i))) + str(i)
            else:
                s = str(i)
            if s[0] == '6':
                s = s + '.SH'
            else:
                s = s + '.SZ'
            if len(s_codes) == 0:
                s_codes = [s]
            else:
                s_codes.append(s)
        df2['Wind_Code'] = s_codes
        # 排除st和300、688开头的股票
        dfs = df2[~ df2['Name'].str.contains('ST')]
        last_dfs = dfs[~ dfs['Wind_Code'].str.contains('^300|^688')]
    return last_dfs


def send_tg(date, msg, chat_id):
    token = '723532221:AAH8SSfM7SfTe4HmhV72QdLbOUW3akphUL8'
    bot = Bot(token=token)
    chat_id = chat_id
    text = '<a href="http://data.eastmoney.com/zjlx/detail.html">%s两市资金流向</a>\n' % date + msg
    bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)


def main(date, num, tactics):
    dfs = get_stocks(num)
    display_column = ['Wind_Code', 'Name', 'Type', 'Close', 'Super', 'Big', 'Mid', 'Small', 'Radio']
    df = dfs.loc[
            (dfs["Close"] < 50) &
            (dfs["Super"] > 0) &
            (dfs["Master"] > 0) &
            (dfs["Big"] > 0) &
            (dfs["Mid"] < 0) &
            (dfs["Small"] < 0), display_column
        ]
    df['Increase_1'] = np.nan
    df['Increase_2'] = np.nan
    df['Increase_3'] = np.nan
    df.to_sql(date, con=engine)
    # for tactic in tactics:
    #     # 策略1：超大单从大到小排序，非科创，股价小于60，主力/超大单/大单为正，小单/中单为负，超大单占比小于16，大于10
    #     df = df_a.sort_values([tactic], ascending=[0]).reset_index(drop=True)
    # df1 = df.round({'Buy': 2})[:50].to_string(header=None)
    # df2 = df.round({'Buy': 2})[51:].to_string(header=None)
    # # 发送tg
    # send_tg(date, df1, chat_id)
    # send_tg(date, df2, chat_id)


if __name__ == '__main__':
    t1 = int(time.time() * 1000)
    t2 = t1 - 31
    t = 20
    date_format = '%Y-%m-%d'
    # 获得当天
    dd = datetime.now()
    if dd.hour > t:
        cur_date = dd.strftime(date_format)
    else:
        cur_date = (dd - timedelta(1)).strftime(date_format)
    tactics = ['Master', 'Super', 'Big']
    num = 2000
    main(cur_date, num, tactics)
