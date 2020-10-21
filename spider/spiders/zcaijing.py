# -*- coding: utf-8 -*-
# author: itimor
# description: zcaijing.com spider

import requests
from lxml import etree, html
from markdownify import markdownify

from spider.spiders.django_env import *
code = 'zcaijin'
obj = SpiderInfo.objects.get(code=code)
base_url = obj.base_url

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
        same_blog = [blog.code for blog in all_blog if blog.source == full_blog_url]
        if len(same_blog) > 0:
            print(f"有相同的博客code {same_blog[0]}")
        else:
            new_blog_url_list.append(full_blog_url)
    return new_blog_url_list


def get_category_blog(dt=None):
    all_category = Category.objects.filter(is_root=False)
    all_blog = Article.objects.all()
    new_blog_url_list = []

    for category in all_category:
        print(category)
        category_list = []
        url = base_url + f"/{category.code}/"
        r = requests.get(url).text
        etree_html = etree.HTML(r)

        if dt is not None:
            column_ul = etree_html.xpath('//div[@class="ml-4 juhe-ml-mobile"]')
            for item in column_ul:
                code_date = item.xpath('./span[@class="juhe-page-right-div-time-span"]/text()')[0]
                if code_date == dt:
                    code_url = item.xpath('./h2/a[@class="juhe-page-left-div-link"]/@href')[0]
                    full_blog_url = base_url + code_url
                    same_blog = [blog.code for blog in all_blog if blog.memo == full_blog_url]
                    if len(same_blog) > 0:
                        print(f"有相同的博客code {same_blog[0]}")
                    else:
                        category_list.append(full_blog_url)
        else:
            column_ul = etree_html.xpath('//div[@class="ml-4 juhe-ml-mobile"]')
            for item in column_ul:
                code_url = item.xpath('./h2/a[@class="juhe-page-left-div-link"]/@href')[0]
                full_blog_url = base_url + code_url
                same_blog = [blog.code for blog in all_blog if blog.memo == full_blog_url]
                if len(same_blog) > 0:
                    print(f"有相同的博客code {same_blog[0]}")
                else:
                    category_list.append(full_blog_url)

            page_li = etree_html.xpath('//ul[@class="pagination"]/li[@class="page-item"]')
            page_nums = len(page_li)
            if page_nums > 1:
                for page in range(1, page_nums):
                    url = base_url + f"/{category.code}/p-{page}"
                    new_list = get_signle_category(all_blog, url)
                    category_list += new_list
            print(len(category_list))
            category.number += len(category_list)
        new_blog_url_list += category_list
        category.save()
    return new_blog_url_list


def get_blog(url):
    print(url)
    r = requests.get(url).text
    etree_html = etree.HTML(r)
    title = etree_html.xpath('//div[@class="content-page-header-div d-md-none"]/h1/text()')[0]
    code = os.path.basename(url).split('.')[0]
    footer_info = etree_html.xpath('//div[@class="content-page-meta"]/span/a')
    category_code = footer_info[-2].xpath('./@href')[0].strip('/')
    try:
        category = Category.objects.get(code=category_code)
    except:
        raise Exception(f"{category} 没有创建")
    content = etree_html.xpath('//div[@id="content"]')[0]
    content_imgs = content.xpath('./p/img/@src')
    for img_url in content_imgs:
        full_img_url = base_url + img_url
        a = os.path.split(img_url)
        if a[0] == '/res':
            r = requests.get(full_img_url)
            with open(f'../res/{a[1]}', 'wb') as file:
                file.write(r.content)
    content_html = html.tostring(content).decode("utf-8")
    content = markdownify(content_html, heading_style="ATX")
    tags = footer_info[:-2]
    try:
        Article.objects.create(title=title, code=code, content=content, published=True, category=category, source=url,
                               tags=tags)
    except:
        pass


if __name__ == '__main__':
    count_nums = Counts.objects.get(id=1)
    # 获取单页分类
    # all_blog = Article.objects.all()
    # catagory_url = 'https://www.zcaijing.com/cgzh/'
    # get_signle_category(all_blog, catagory_url)
    # 获取所有分类
    get_category()
    # 获取单个文章
    # blog_url = 'https://www.zcaijing.com/cgzh/198088.html'
    # get_blog(blog_url)
    # 获取所有文章
    all_url = get_category_blog()
    print(len(all_url))
    for blog_url in all_url:
        get_blog(blog_url)
    # 获得当天日志
    # cur_date = time.strftime('%Y-%m-%d')
    # all_url = get_category_blog(cur_date)
    # print(len(all_url))
    # for blog_url in all_url:
    #     get_blog(blog_url)