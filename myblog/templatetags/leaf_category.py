# -*- coding: utf-8 -*-
# author: itimor

from django import template
from myblog.models import Category

register = template.Library()  # 自定义filter时必须加上


@register.filter(is_safe=True)  # 注册template filter
def leaf_category(value):
    all_category = Category.objects.filter(parent=value)
    return all_category
