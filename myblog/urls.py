# -*- coding: utf-8 -*-
# author: itimor

from django.conf.urls import url

from myblog.views import *
from myblog.feeds import ArticleRssFeed

app_name = 'blog'
urlpatterns = [
    # 首页
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^archives/$', ArchiveView.as_view(), name='archives'),
    url(r'^detail/(?P<slug>[\w-]+).html$', ArticleDetailView.as_view(), name='blog-detail'),
    url(r'^tags/$', TagView.as_view(), name='tags'),
    url(r'^tags/(?P<id>\d+)', TagView.as_view(), name="tag-detail"),
    url(r'^categorys/$', CategoryView.as_view(), name='categorys'),
    url(r'^category/(?P<slug>[\w-]+)', CategoryView.as_view(), name="category-detail"),
    # url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^rss/$', ArticleRssFeed(), name='rss'),
    url(r'^links/$', LinkView.as_view(), name="link"),
    # 搜索
    url(r'^search/', SearchView(), name='search'),
]