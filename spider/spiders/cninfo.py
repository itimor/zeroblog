# -*- coding: utf-8 -*-
# author: itimor

import requests
from fake_useragent import UserAgent
from datetime import datetime, timedelta

from utils.index import gen_markdown_table

from spider.spiders.django_env import *

code = 'cninfo'
obj = SpiderInfo.objects.get(code=code)
base_url = obj.base_url

ua = UserAgent()

headers = {'Accept': 'application/json, text/javascript, */*; q=0.01',
           "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
           "Accept-Encoding": "gzip, deflate",
           "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7,zh-HK;q=0.6,zh-TW;q=0.5",
           'Host': 'www.cninfo.com.cn',
           'Origin': 'http://www.cninfo.com.cn',
           'Referer': 'http://www.cninfo.com.cn/new/commonUrl?url=disclosure/list/notice',
           'X-Requested-With': 'XMLHttpRequest',
           'User-Agent': ua.random
           }

url = f'{base_url}/new/hisAnnouncement/query'


def szseAnnual(searchkey, seDate, page=1):
    query = {'pageNum': page,
             'pageSize': 30,
             'tabName': 'fulltext',
             'column': 'szse',
             'searchkey': searchkey,
             'secid': '',
             'plate': 'sz',
             'trade': '',
             'seDate': seDate
             }
    r = requests.post(url, headers=headers, data=query).json()
    return r


def setDate(day=0):
    choose_day = (dt - timedelta(day)).strftime("%Y-%m-%d")
    return f'{choose_day}~{today}'


def timeStamp2datetime(timeStamp):
    d = datetime.fromtimestamp(timeStamp)
    ds = d.strftime("%Y-%m-%d")
    return ds


def save_blog(title, content, category, tags, source):
    try:
        Article.objects.update_or_create(title=title, published=True, category=category, source=source, defaults={
            "content": content, "tags": tags
        })
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    dt = datetime.now()
    today = dt.strftime("%Y-%m-%d")
    start_day = (dt - timedelta(3)).strftime("%Y-%m-%d")
    end_day = (dt - timedelta(1)).strftime("%Y-%m-%d")
    seDate = f'{start_day}~{end_day}'
    print(seDate)
    data = []
    searchkeys = obj.keyword
    for searchkey in searchkeys.split():
        print(searchkey)
        p = szseAnnual(searchkey, seDate)
        total_num = p['totalRecordNum']

        if total_num:
            data += p['announcements']
        if total_num > 30:
            page_total = int(total_num / 30)
            for page in range(1, page_total + 1):
                p = szseAnnual(searchkey, seDate, page)
                if p['announcements'] is not None:
                    data += p['announcements']
        print(data)
    b = []
    for i in data:
        i['announcementTime'] = timeStamp2datetime(i['announcementTime'] / 1000)
        new_url = f"{base_url}/new/disclosure/detail?stockCode={i['secCode']}&announcementId={i['announcementId']}&orgId={i['orgId']}&announcementTime={i['announcementTime']}'"
        i['announcementTitle'] = f"[{i['announcementTitle']}]({new_url})" + "{:target='_blank'}"
        b.append(i)
    header = ["代码", "简称", "标题", "时间"]
    header_code = ["secCode", "secName", "announcementTitle", "announcementTime"]
    all_data = gen_markdown_table(header, header_code, b)
    category = Category.objects.get(name=obj.name)
    if len(b) > 2:
        save_blog(f'{title}-{cur_date}', home_content, blog_category, ' '.join(tags), source)
        Article.objects.update_or_create(title=f'{obj.name}-{today}', code=today, content=all_data, published=True,
                                         category=category, tags=searchkeys, allow_comments=False)
    print(all_data)
