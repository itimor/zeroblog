# -*- coding: utf-8 -*-
# author: itimor

import markdown

from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

register = template.Library()  # 自定义filter时必须加上

md = markdown.Markdown(
    safe_mode=True,
    enable_attributes=False,
    extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.toc',
        'markdown.extensions.codehilite',
        'markdown.extensions.fenced_code',
    ])


@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def custom_markdown(value):
    return mark_safe(md.convert(value))


@register.filter(is_safe=True)  # 注册template filter
@stringfilter  # 希望字符串作为参数
def custom_markdown_summary(value):
    # 截取readmore前的字符串作为摘要并用markdown渲染
    readmore_index = finding_nemo(value, '\n', 3)
    content = value[:readmore_index]
    if len(content) < 100:
        readmore_index = finding_nemo(value, '\n', 5)
        content = value[:readmore_index]
    return mark_safe(md.convert(content))


def finding_nemo(String, Substr, times):
    String_list = String.split(Substr, times)
    nemo = len(String) - len(String_list[-1]) - 1
    return nemo
