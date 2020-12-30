# -*- coding: utf-8 -*-
# 实现， 东方财富的 龙虎榜爬虫
import pandas as pd
import numpy as np
from scrapy import Selector
import datetime
import time
import re
import requests


def dateRange(start, end, step=1, format="%Y-%m-%d"):
    strptime, strftime = datetime.datetime.strptime, datetime.datetime.strftime
    days = (strptime(end, format) - strptime(start, format)).days
    return [strftime(strptime(start, format) + datetime.timedelta(i), format) for i in range(0, days + 1, step)]


def Get_LHB_stocks_from_excel(begin_date, end_date):
    Timeline = dateRange(begin_date, end_date)
    dfs = pd.DataFrame()
    for date_id in Timeline:
        URL_stocks_infos = r'http://data.eastmoney.com/DataCenter_V3/stock2016/TradeDetail/pagesize=200,page=1,sortRule=-1,sortType=,startDate=' + date_id + ',endDate=' + date_id + ',gpfw=0,js=var%20data_tab_1.html?rt=26442172'
        r = requests.get(URL_stocks_infos).text
        X = re.split(',"url"', r)[0]
        X = re.split('"data":', X)[1]
        df = pd.read_json(X, orient='records')
        if (len(df) != 0):
            df2 = df[
                ['Tdate', 'SCode', 'SName', 'ClosePrice', 'JmRate', 'Dchratio', 'Ltsz', 'JD']]
            colunms_name = ['Code', 'Name', '收盘价', '净买额占比', '换手率', '流通市值', '买卖方', '成功率']
            df2 = df2.rename(
                columns={'Tdate': 'Date', 'SCode': colunms_name[0], 'SName': colunms_name[1],
                         'ClosePrice': colunms_name[3], 'JmRate': colunms_name[10], 'Ltsz': colunms_name[13]})
            df2['Wind_Code'] = str(df2['Code'])
            s_codes = list()
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
            print('Date: ', date_id, '上榜条数: ', len(df2), ',  上榜股票只数: ', len(df2['Wind_Code'].unique()))
            dfs = dfs.append(df2)
        else:
            print('Date: ', date_id, '上榜条数: ', 0, ',  上榜股票只数: ', 0)
    return dfs


def main(begin_date, end_date):
    Stocks_info = Get_LHB_stocks_from_excel(begin_date, end_date)
    Timeline_unique = np.unique(Stocks_info['Date'])
    str_result_filename = "龙虎榜综合信息_" + str(min(Stocks_info['Date'])) + '_' + str(max(Stocks_info['Date'])) + ".xlsx"
    print(str_result_filename)
    print(Stocks_info)
    print(Timeline_unique)


########### main function ########################
if __name__ == '__main__':
    save_dir = '/Users/sha/data/longhu/'
    begin_date = '2020-12-30'
    end_date = '2020-12-30'
    main(begin_date, end_date)
