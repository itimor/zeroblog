# -*- coding: utf-8 -*-
# author: itimor

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView, DetailView
from django.db.models import Count
from myblog.models import Article, Category, Friend
from utils.paginations import get_pagination
import markdown
from taggit.models import Tag
from pure_pagination import PageNotAnInteger, Paginator
from haystack.views import SearchView as HaystackSearchView
from blog.settings import HAYSTACK_SEARCH_RESULTS_PER_PAGE

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
    context_object_name = "blog_posts"
    queryset = Article.objects.filter(status='p')

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        try:
            page = self.request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 5
        page_data = get_pagination(self.queryset, page, request=self.request)
        context['page_data'] = page_data
        return context


class ArticleDetailView(BaseMixin, DetailView):
    """
    文章详情
    """
    template_name = "article-detail.html"
    context_object_name = "post"
    queryset = Article.objects.filter(status='p')

    def get_object(self, queryset=None):
        context = super(ArticleDetailView, self).get_object()

        if context.status != 'p':
            raise PermissionDenied

        # 阅读数增1
        context.views += 1
        context.save(modified=False)
        context.content = md.convert(context.content)
        return context

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data(**kwargs)
        current_post = context.get("object")

        # 实现博客上一篇与下一篇功能
        has_prev = False
        has_next = False
        id_prev = id_next = int(current_post.id)
        blog_id_max = Article.objects.all().order_by('-id').first()
        id_max = blog_id_max.id
        prev_post = None
        next_post = None
        while not has_prev and id_prev >= 1:
            prev_post = Article.objects.filter(id=id_prev - 1).first()
            if not prev_post:
                id_prev -= 1
            else:
                has_prev = True
        while not has_next and id_next <= id_max:
            next_post = Article.objects.filter(id=id_next + 1).first()
            if not next_post:
                id_next += 1
            else:
                has_next = True

        context['prev_post'] = prev_post
        context['next_post'] = next_post
        return context


class TagView(BaseMixin, ListView):
    template_name = 'tags.html'
    context_object_name = "tag_posts"
    queryset = Article.objects.filter(status='p')

    def get_context_data(self, **kwargs):
        context = super(TagView, self).get_context_data(**kwargs)
        tag_id = self.kwargs.get('id')
        if tag_id:
            tag = get_object_or_404(Tag, id=tag_id)
            queryset = Article.objects.filter(tags__in=[tag]).order_by('is_top', '-id')
            try:
                page = self.request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 5
            page_data = get_pagination(queryset, page, request=self.request)
            context['page_data'] = page_data
            context['tag'] = tag
        else:
            queryset = Tag.objects.all().annotate(number=Count('article'))
        context['object_list'] = queryset
        return context


class CategoryView(BaseMixin, ListView):
    template_name = 'categorys.html'
    context_object_name = "category_posts"
    queryset = Article.objects.filter(status='p')

    def get_context_data(self, **kwargs):
        context = super(CategoryView, self).get_context_data(**kwargs)
        print(context)
        category_slug = self.kwargs.get('slug')

        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
            queryset = Article.objects.filter(category__slug=category_slug).order_by('is_top', '-id')
            try:
                page = self.request.GET.get('page', 1)
            except PageNotAnInteger:
                page = 5
            page_data = get_pagination(queryset, page, request=self.request)
            context['page_data'] = page_data
            context['category'] = category
        else:
            queryset = Tag.objects.all().annotate(number=Count('article'))
        context['object_list'] = queryset
        return context


class ArchiveView(BaseMixin, ListView):
    template_name = 'archive.html'
    context_object_name = "archive_posts"
    queryset = Article.objects.filter(status='p').order_by("-publish_time")

    def get_context_data(self, **kwargs):
        context = super(ArchiveView, self).get_context_data(**kwargs)
        return context


class LinkView(BaseMixin, ListView):
    template_name = 'links.html'
    context_object_name = "links_posts"
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
