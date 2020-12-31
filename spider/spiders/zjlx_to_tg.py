# -*- coding: utf-8 -*-
# author: itimor
# 东方财富资金流向，并根据策略筛选股票，并发送到tg频道

from datetime import datetime, timedelta
from telegram import Bot, ParseMode
from fake_useragent import UserAgent
import pandas as pd
import numpy as np
import time
import re
import requests
import math

ua = UserAgent()

headers = {'User-Agent': ua.random}


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
        s_types = []
        for i in df2['Code']:
            if len(str(i)) < 6:
                s = '0' * (6 - len(str(i))) + str(i)
            else:
                s = str(i)
            if s[0] == '6':
                s_type = 'SH'
            elif s[0] == '3':
                s_type = 'KC'
            else:
                s_type = 'SZ'
            if len(s_codes) == 0:
                s_codes = [s]
                s_types = [s_type]
            else:
                s_codes.append(s)
                s_types.append(s_type)
        df2['Wind_Code'] = s_codes
        df2['Type'] = s_codes
        dfs = df2[~ df2['Name'].str.contains('ST')]
    return dfs


def send_tg(date, msg, chat_id):
    token = '723532221:AAH8SSfM7SfTe4HmhV72QdLbOUW3akphUL8'
    bot = Bot(token=token)
    chat_id = chat_id
    text = '<a href="http://data.eastmoney.com/zjlx/detail.html">%s两市资金流向</a>\n' % date + msg
    bot.send_message(chat_id=chat_id, text=text, parse_mode=ParseMode.HTML)


def main(date, num=1000, max=50, tactics='df1'):
    dfs = get_stocks(num)
    display_column = ['Wind_Code', 'Name', 'Type', 'Close', 'Super']
    chat_id = ""
    df_a = pd.DataFrame()
    if tactics == 'df1':
        # 策略1：超大单从大到小排序，非科创，股价小于50，主力/超大单/大单为正，小单/中单为负，超大单占比小于16，大于0
        df_a = dfs.loc[
            (dfs["Close"] < 50) &
            (dfs["Super"] > 0) &
            (dfs["Super"] < 15) &
            (dfs["Master"] > 0) &
            (dfs["Big"] > 0) &
            (dfs["Mid"] < 0) &
            (dfs["Small"] < 0) &
            (dfs["Type"] != "KC"), display_column
        ].sort_values(['Super'], ascending=[0])
        chat_id = "@timorstock"

    df = df_a.reset_index(drop=True)[:max]
    b = [1 / math.log(i + 2) for i in range(0, len(df))]
    df['Buy'] = [i / sum(b) for i in b]
    df[['Close']] = df[['Close']].astype(float)
    df['BuyCount'] = df['Buy'] / df['Close']
    print(df)
    last_df = df.round({'Buy': 2}).to_string(header=None)
    # 发送tg
    if len(last_df) > 0:
        send_tg(date, last_df, chat_id)


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
    tactics = 'df1'
    num = 1000
    max = 100
    main(cur_date, num, max, tactics)
