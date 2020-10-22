# -*- coding: utf-8 -*-
# author: itimor

from django.conf.urls import url

from myblog.views import *
from myblog.feeds import ArticleRssFeed

urlpatterns = [
    url(r'^archive/$', ArichiveView.as_view(), name='archive'),
    url(r'^detail/(?P<blog_code>\w+).html$', ArticleDetailView.as_view(), name='blog_code'),
    url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^rss/$', ArticleRssFeed(), name='rss'),
    url(r'^categorys/$', CategoryView.as_view(), name='categorys'),
    url(r'^category/(?P<category_code>[\w,-]+)/$', CategoryDetaiView.as_view(), name='category_code'),
]