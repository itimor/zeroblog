# -*- coding: utf-8 -*-
# author: itimor

from django.conf.urls import url

from myblog.views import *
from myblog.feeds import ArticleRssFeed
from myblog.error_views import bad_request, permission_denied, page_not_found, server_error

# 定义错误跳转页面
handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error

app_name = 'blog'
urlpatterns = [
    # 首页
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^archives/$', ArchiveView.as_view(), name='archives'),
    url(r'^detail/(?P<blog_slug>\w+).html$', ArticleDetailView.as_view(), name='blog_slug'),
    # url(r'^add_comment/$', AddCommentView.as_view(), name='add_comment'),
    url(r'^rss/$', ArticleRssFeed(), name='rss'),
    url(r'^tags/$', TagView.as_view(), name='tags'),
    url(r'^tag/(?P<tag>\w+)', TagView.as_view(), name="tag-detail"),
    # url(r'^tag/(?P<tag_id>\d+)/$', TagDetailView.as_view(), name='tag_id'),
    # url(r'^categorys/$', CategoryView.as_view(), name='categorys'),
    # url(r'^category/(?P<category_slug>[\w,-]+)/$', CategoryDetaiView.as_view(), name='category_slug'),
    url(r'^link/', LinkView.as_view(), name="link"),
    # 搜索
    url(r'^search/', SearchView(), name='search'),
]