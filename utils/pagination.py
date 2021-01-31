# -*- coding: utf-8 -*-
# author: itimor

from pure_pagination import PageNotAnInteger, Paginator


def get_pagination(posts, page, request):
    nums = len(posts)
    if nums < 50:
        num = 5
    elif nums < 100:
        num = 10
    elif nums < 500:
        num = 20
    else:
        num = 30
    p = Paginator(posts, num, request=request)
    posts = p.page(page)
    return posts
