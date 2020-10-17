# -*- coding: utf-8 -*-
# author: itimor
# description: zcaijing.com spider

import requests
from lxml import etree, html
import os
import django
from markdownify import markdownify

os.environ['DJANGO_SETTINGS_MODULE'] = 'blog.settings'
django.setup()

from myblog.models import Category, Tag, Blog

base_url = "https://www.zcaijing.com"

ignore_category1 = ['k线图', '移动平均线', 'MACD', '股票技术指标', '股票大盘', '涨停板预测', '分时图', '股市名家', '缠中说禅', '股票投资', '期货', '股票黑马',
                    '美股要闻', '市场动向', '主力研究', '炒股软件', '投稿专区', '股票公式', '股市战法', '大V论市', '基金', '黄金', '私募投资']
ignore_category2 = ['港股投资入门', '缠论解盘', '缠论108课']


def get_category():
    url = base_url
    r = requests.get(url).text
    etree_html = etree.HTML(r)
    column_ul = etree_html.xpath('//div[@class="content"]/ul[@class="column_ul"]')

    for ul in column_ul:
        column_li = ul.xpath('./li')
        tag1_li = column_li[0]
        code = tag1_li.xpath('./a/@href')[0].strip('/')
        name = tag1_li.xpath('./a/text()')[0]
        if name in ignore_category1:
            continue
        tag2_li = column_li[1::]
        parent, _ = Category.objects.update_or_create(name=name, code=code, defaults={
            "parent": None, "is_root": True, "number": len(tag2_li)})

        for li in tag2_li:
            code = li.xpath('./a/@href')[0].strip('/')
            name = li.xpath('./a/text()')[0]
            if name in ignore_category2:
                continue
            Category.objects.update_or_create(name=name, code=code, defaults={"parent": parent, "is_root": False})


def get_signle_category(all_blog, url):
    new_blog_url_list = []
    r = requests.get(url).text
    etree_html = etree.HTML(r)
    column_ul = etree_html.xpath('//a[@class="juhe-page-left-div-link"]/@href')
    for code_url in column_ul:
        full_blog_url = base_url + code_url
        same_blog = [blog.code for blog in all_blog if blog.memo == full_blog_url]
        if len(same_blog) > 0:
            print(f"有相同的博客code {same_blog[0]}")
        else:
            new_blog_url_list.append(full_blog_url)
    return new_blog_url_list


def get_category_blog():
    all_category = Category.objects.filter(is_root=False)
    all_blog = Blog.objects.all()
    new_blog_url_list = []

    for category in all_category:
        url = base_url + f"/{category.code}/"
        r = requests.get(url).text
        etree_html = etree.HTML(r)
        page_li = etree_html.xpath('//ul[@class="pagination"]/li[@class="page-item"]')
        page_nums = len(page_li)
        if page_nums > 1:
            for page in range(1, page_nums):
                url = base_url + f"/{category.code}/p-{page}"
                new_list = get_signle_category(all_blog, url)
                new_blog_url_list += new_list
        column_ul = etree_html.xpath('//a[@class="juhe-page-left-div-link"]/@href')
        for code_url in column_ul:
            full_blog_url = base_url + code_url
            same_blog = [blog.code for blog in all_blog if blog.memo == full_blog_url]
            if len(same_blog) > 0:
                print(f"有相同的博客code {same_blog[0]}")
            else:
                new_blog_url_list.append(full_blog_url)
    return new_blog_url_list


def get_blog(url):
    r = requests.get(url).text
    etree_html = etree.HTML(r)
    title = etree_html.xpath('//div[@class="content-page-header-div d-md-none"]/h1/text()')[0]
    code = os.path.basename(url)
    footer_info = etree_html.xpath('//div[@class="content-page-meta"]/span/a')
    category_code = footer_info[-2].xpath('./@href')[0].strip('/')
    try:
        category = Category.objects.get(code=category_code)
    except:
        raise Exception(f"{category} 没有创建")
    content = etree_html.xpath('//div[@id="content"]')
    content_html = html.tostring(content[0]).decode("utf-8")
    content = markdownify(content_html, heading_style="ATX")
    blog = Blog.objects.create(title=title, code=code, content=content, published=True, category=category)
    tags = footer_info[:-2]
    for item in tags:
        code = item.xpath('./@href')[0].strip('/')
        name = item.xpath('./text()')[0]
        tag, s = Tag.objects.get_or_create(name=name, defaults={"code": code})
        if s:
            blog.tag.add(tag)


if __name__ == '__main__':
    # # 获取所有分类
    # get_category()
    # # 获取单页分类
    # all_blog = Blog.objects.all()
    # catagory_url = 'https://www.zcaijing.com/cgzh/'
    # get_signle_category(all_blog, catagory_url)
    # 获取所有分类
    all_url = get_category_blog()
    for blog_url in all_url:
        print(blog_url)
        # 获取单个文章
        # blog_url = 'https://www.zcaijing.com/cgzh/198088.html'
        get_blog(blog_url)
