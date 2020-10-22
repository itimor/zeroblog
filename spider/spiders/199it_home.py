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
    {'name': '研究报告', 'code': 'report', 'active': True, 'is_today': False, 'many': False},
]

# 爬虫时间最好设置在每天9点前
t = 9
# 文章标题
title = '199it报告'


def get_blog(url, dt):
    blog_url_list = []
    r = requests.get(url).text
    etree_html = etree.HTML(r)
    column_ul = etree_html.xpath('//article/div[@class="entry-content"]')
    for item in column_ul:
        code_date = item.xpath('./aside[@class="meta-row row-3"]/div/ul/li[@class="post-time"]/time/text()')[0]
        title = item.xpath('./h2/a/text()')[0]
        tags = item.xpath('./aside[@class="meta-row cat-row"]/div/ul/li/a/text()')
        if code_date == dt:
            code_url = item.xpath('./h2/a/@href')[0]
            data = {
                'url': code_url,
                'title': title,
                'tags': tags[:-1],
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
            cur_date = dd.strftime(date_format)
        else:
            if dd.hour > t:
                cur_date = dd.strftime(date_format)
            else:
                cur_date = (dd - timedelta(1)).strftime(date_format)
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
                d = {'title': f"[{pp['title']}]({pp['url']})" + "{:target='_blank'}", 'tag': ' '.join(tag),
                     'date': cur_date}
                data.append(d)
        home_content += gen_markdown_table(header, header_code, data)
        home_content += "\n"
        home_content += "\n"
        tags = list(set(tags))
    source = base_url
    try:
        blog_category = Category.objects.get(name=title)
    except:
        raise Exception(f"{blog_category} 没有创建")
    save_blog(f'{title}-{cur_date}', cur_date, home_content, blog_category, ' '.join(tags), source)
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
    category = '199it'
    date_format = '%Y年%m月%d日'
    base_url = 'http://www.199it.com/archives/category'
    p = make_home(single_urls)
    # test
    # p = get_blog('http://www.199it.com/archives/category/report', '2020年10月21日')
    print(p)
