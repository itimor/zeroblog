# -*- coding: utf-8 -*-
# author: itimor

from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from myblog.models import Article, Friend
from utils.pagination import get_pagination
import markdown
from taggit.models import Tag
from pure_pagination import PageNotAnInteger, Paginator
from haystack.views import SearchView as HaystackSearchView


md = markdown.Markdown(
    safe_mode=True,
    enable_attributes=False,
    extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.toc',
        'markdown.extensions.codehilite',
        'markdown.extensions.fenced_code',
    ])


class BaseMixin(object):
    def get_context_data(self, **kwargs):
        context = super(BaseMixin, self).get_context_data(**kwargs)
        return context


class IndexView(BaseMixin, ListView):
    """
    首页
    """
    template_name = 'index.html'
    context_object_name = "all_blog"
    queryset = Article.objects.filter(status='p')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)

        # 父类生成的字典中已有 paginator、page_obj、is_paginated 这三个模板变量，
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')

        # 调用自己写的 pagination_data 方法获得显示分页导航条需要的数据，见get_pagination()。
        pagination_data = get_pagination(paginator, page, is_paginated)

        # 将分页导航条的模板变量更新到 context 中，注意 pagination_data 方法返回的也是一个字典。
        context.update(pagination_data)
        return context


class ArticleDetailView(BaseMixin, DetailView):
    """
    文章详情
    """
    template_name = "detail.html"
    context_object_name = "post"
    queryset = Article.objects.filter(status='p')

    def get_object(self, queryset=None):
        context = super(ArticleDetailView, self).get_object()

        if context.status != 'p':
            raise PermissionDenied

        # 阅读数增1
        context.views += 1
        context.save(modified=False)

        import re
        re.sub(r'--more--', '', context.content)

        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])

        context.content = md.convert(context.content)

        return context

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        current_post = context.get("object")

        prev_post = None
        next_post = None

        try:
            prev_post = Article.objects.get(status='p', pk=(current_post.id - 1))
        except Exception as e:
            print(e)

        try:
            next_post = Article.objects.get(status='p', pk=(current_post.id + 1))
        except Exception as e:
            print(e)

        context['prev_post'] = prev_post
        context['next_post'] = next_post
        return context


class TagView(BaseMixin, ListView):
    """
    首页
    """
    template_name = 'tag.html'
    context_object_name = "tag_posts"
    queryset = Article.objects.filter(status='p')

    def get_queryset(self):
        tag = self.kwargs.get('tag')
        json_tags = []

        if tag:
            context = super(TagView, self).get_queryset().filter(tags__slug=tag)
            return {'tag': tag, 'posts': context, 'json_tags': json_tags}
        else:
            from django.db.models import Count
            context = Tag.objects.all()
            queryset = context.annotate(num_times=Count('taggit_taggeditem_items'))
            for tag in queryset:
                json_tags.append({"name": tag.name, "slug": tag.slug, "count": tag.num_times})
            return {'json_tags': json_tags}


class ArchiveView(BaseMixin, ListView):
    """
    首页
    """
    template_name = 'archive.html'
    context_object_name = "archive_posts"
    queryset = Article.objects.filter(status='p').order_by("-publish_time")

    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)
        return context


class LinkView(BaseMixin, ListView):
    """
    首页
    """
    template_name = 'link.html'
    context_object_name = "posts"
    queryset = Friend.objects.filter(active=True)

    def get_context_data(self, **kwargs):
        context = super(LinkView, self).get_context_data(**kwargs)
        return context


class SearchView(HaystackSearchView):
    """
    复用搜索源码，将其余内容添加进来
    """

    def extra_context(self):
        context = super(SearchView, self).extra_context()
        return context

    def build_page(self):
        # 分页重写
        super(SearchView, self).extra_context()

        try:
            page_no = int(self.request.GET.get('page', 1))
        except PageNotAnInteger:
            raise HttpResponse("Not a valid number for page.")

        if page_no < 1:
            raise HttpResponse("Pages should be 1 or greater.")

        paginator = Paginator(self.results, HAYSTACK_SEARCH_RESULTS_PER_PAGE, request=self.request)
        page = paginator.page(page_no)

        return (paginator, page)

