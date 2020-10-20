# -*- coding: utf-8 -*-
# author: itimor

from django import template
from myblog.models import Article, Category

register = template.Library()  # 自定义filter时必须加上


# 博客、标签、分类数目统计
@register.filter(is_safe=True)  # 注册template filter
def count_nums(value):
    d = 0
    if value == 'blog':
        d = Article.objects.filter(published=True).count()
    if value == 'cate':
        d = Category.objects.all().count()
    return d
