# -*- coding: utf-8 -*-
# author: itimor
# description: zcaijing.com 爬取首页的一些板块内容

import requests
from lxml import etree, html
from datetime import datetime, timedelta

from spider.spiders.django_env import *
from utils.index import gen_markdown_table

# 单独页面
single_urls = [
    {'name': '股市要闻', 'code': 'gushiyaowen', 'active': True, 'is_today': True, 'many': True},
    {'name': '市场动向', 'code': 'scdx', 'active': True, 'is_today': True, 'many': True},
]
# 聚合首页
group_urls = [
    {'name': '上证早知道', 'code': 'szzzd', 'active': True, 'is_today': False, 'many': False},
    {'name': '新股要闻', 'code': 'xgyw', 'active': True, 'is_today': False, 'many': False},
    {'name': '主力研究', 'code': 'zlyj', 'active': True, 'is_today': False, 'many': False},
    {'name': '分析上市公司', 'code': 'shangshigongsi', 'active': True, 'is_today': False, 'many': False},
    {'name': '行业资讯', 'code': 'hyzx', 'active': True, 'is_today': False, 'many': True},
    {'name': '宏观经济', 'code': 'hongguan', 'active': True, 'is_today': False, 'many': True},
]

# 爬虫时间最好设置在每天9点前
t = 9
# 文章标题
title = '零点简报-%s'


def get_blog(url, dt):
    blog_url_list = []
    r = requests.get(url).text
    etree_html = etree.HTML(r)
    if url == 'https://www.zcaijing.com/szzzd/':
        column_ul = etree_html.xpath('//div[@class="ml-4 juhe-ml-mobile"]')
    else:
        column_ul = etree_html.xpath('//div[@class="d-flex flex-row my-3"]/div[@class="ml-0"]')
    for item in column_ul:
        code_date = item.xpath('./span[@class="juhe-page-right-div-time-span"]/text()')[0]
        title = item.xpath('./h2/a[@class="juhe-page-left-div-link"]/text()')[0]
        tags = item.xpath('./span[@class="juhe-page-left-div-keyword-span"]/a/text()')
        if code_date == dt:
            code_url = item.xpath('./h2/a[@class="juhe-page-left-div-link"]/@href')[0]
            full_blog_url = base_url + code_url
            data = {
                'url': full_blog_url,
                'title': title,
                'tags': tags,
            }
            blog_url_list.append(data)
    return blog_url_list


def make_home(zcaijing_urls):
    home_content = ''
    header = ["标题", "关键字", "日期"]
    header_code = ["title", "tag", "date"]
    tags = []
    for item in zcaijing_urls:
        print(item['name'])
        home_content += f"## {item['name']}"
        home_content += "\n"
        page_code = item['code']
        # 获得当天
        dd = datetime.now()
        if item['is_today']:
            cur_date = dd.strftime('%Y-%m-%d')
        else:
            if dd.hour > t:
                cur_date = dd.strftime('%Y-%m-%d')
            else:
                cur_date = (dd - timedelta(1)).strftime('%Y-%m-%d')
        if item['many']:
            urls = [f'{base_url}/{page_code}/p-0/', f'{base_url}/{page_code}/p-1/']
        else:
            urls = [f'{base_url}/{page_code}/']
        p = []
        for url in urls:
            a = get_blog(url, cur_date)
            p += a
        if len(p) > 0:
            data = []
            for pp in p:
                tag = [i.strip() for i in pp['tags']]
                tags += tag
                # home_content += f"- [{pp['title']}]({pp['url']})" + "{:target='_blank'}" + ','.join(tag)
                # home_content += "\n"
                d = {'title': f"[{pp['title']}]({pp['url']})" + "{:target='_blank'}", 'tag': ' '.join(tag), 'date': cur_date}
                data.append(d)
        home_content += gen_markdown_table(header, header_code, data)
        home_content += "\n"
        home_content += "\n"
        tags = list(set(tags))
    source = base_url
    try:
        blog_category = Category.objects.get(name='零点简报')
    except:
        raise Exception(f"{blog_category} 没有创建")
    save_blog(title % cur_date, home_content, blog_category, ' '.join(tags), source)
    return home_content


def save_blog(title, content, category, tags, source):
    try:
        Article.objects.update_or_create(title=title, published=True, category=category, source=source, defaults={
            "content": content, "tags": tags
        })
    except Exception as e:
        print(e)
        pass


if __name__ == '__main__':
    category = 'zcaijing'
    obj = SpiderInfo.objects.get(code=category)
    base_url = obj.base_url
    p = make_home(group_urls)
    p = make_home(single_urls)
    # test
    # p = get_blog('https://www.zcaijing.com/hongguan/', '2020-10-21')
    print(p)
