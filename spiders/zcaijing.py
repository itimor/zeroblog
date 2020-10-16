# -*- coding: utf-8 -*-
# author: itimor
# description: zcaijing.com spider

import requests
import re
from lxml import etree
import os
import django

os.environ['DJANGO_SETTINGS_MODULE'] = 'blog.settings'
django.setup()

from myblog.models import *

ignore_category1 = ['k线图', '移动平均线', 'MACD', '股票技术指标', '股票大盘', '涨停板预测', '分时图', '股市名家', '缠中说禅', '股票投资', '期货', '股票黑马',
                    '美股要闻', '市场动向', '主力研究', '炒股软件', '投稿专区', '股票公式', '股市战法', '大V论市', '基金', '黄金', '私募投资']
ignore_category2 = ['港股投资入门', '缠论解盘', '缠论108课']

url = "https://www.zcaijing.com"
r = requests.get(url).text
html = etree.HTML(r)
column_ul = html.xpath('//div[@class="content"]/ul[@class="column_ul"]')

for ul in column_ul:
    column_li = ul.xpath('./li')
    tag1_li = column_li[0]
    code = tag1_li.xpath('./a/@href')[0].strip('/')
    name = tag1_li.xpath('./a/text()')[0]
    if name in ignore_category1:
        continue
    tag2_li = column_li[1::]
    guo_li = []
    for li in tag2_li:
        code = li.xpath('./a/@href')[0].strip('/')
        name = li.xpath('./a/text()')[0]
        if name in ignore_category2:
            continue
        url = f"https://www.zcaijing.com/{code}/"
        r = requests.get(url).text
        html = etree.HTML(r)
        page_li = html.xpath('//ul[@class="pagination"]/li[@class="page-item"]')
        page_nums = len(page_li)
        if page_nums > 1:
            for page in range(1, page_nums):
                url = f"https://www.zcaijing.com/{code}/p-{page}"
