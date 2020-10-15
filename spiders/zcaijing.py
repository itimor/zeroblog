# -*- coding: utf-8 -*-
# author: itimor
# description: zcaijing.com spider

import requests
import re
from lxml import etree

# 忽略爬取
ignore_tag1 = ['涨停板预测', '美股要闻', '市场动向', '主力研究', '热点专题', '股市名家', '炒股软件', '投稿专区', '股票公式', '股市战法', '大V论市', '基金', '黄金',
               'MACD', '移动平均线', 'k线图', '股票技术指标']
ignore_tag2 = ['港股投资入门', '缠论解盘', '缠论108课']

url = "https://www.zcaijing.com"
r = requests.get(url).text
html = etree.HTML(r)
column_ul = html.xpath('//div[@class="content"]/ul[@class="column_ul"]')

for ul in column_ul:
    column_li = ul.xpath('./li')
    tag1_li = column_li[0]
    code = tag1_li.xpath('./a/@href')[0].strip('/')
    name = tag1_li.xpath('./a/text()')[0]
    if name in ignore_tag1:
        continue
    tag2_li = column_li[1::]
    guo_li = []
    for li in tag2_li:
        code = li.xpath('./a/@href')[0].strip('/')
        name = li.xpath('./a/text()')[0]
        if name in ignore_tag2:
            continue
        url = f"https://www.zcaijing.com/{code}/"
        r = requests.get(url).text
        html = etree.HTML(r)
        column_ul = html.xpath('//div[@class="content"]/ul[@class="column_ul"]')
