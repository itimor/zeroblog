# -*- coding: utf-8 -*-
# author: itimor

import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()  #自定义filter时必须加上

md = markdown.Markdown(
    safe_mode=True,
    enable_attributes=False,
    extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.toc',
        'markdown.extensions.codehilite',
        'markdown.extensions.fenced_code',
    ])

@register.filter(is_safe=True)  #注册template filter
@stringfilter  #希望字符串作为参数
def custom_markdown(value):
    return mark_safe(md.convert(value))

@register.filter(is_safe=True)  #注册template filter
@stringfilter  #希望字符串作为参数
def custom_markdown_summary(value):
    # 生成摘要
    try:
        # 获取readmore位置
        readmore_index = value.find('<!--more-->')

        # 截取readmore前的字符串作为摘要并用markdown渲染
        content = value[:readmore_index]
    except:
        content = value[:100]
    return mark_safe(md.convert(content))