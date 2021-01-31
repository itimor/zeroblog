from django.db import models
from mdeditor.fields import MDTextField
from django.utils import timezone
from django.utils.html import format_html
from django.urls import reverse
from uuslug import slugify
from taggit.managers import TaggableManager
from utils.db import BaseModel
from utils.index import get_hash, get_cover


class Category(BaseModel):
    """
    博客分类
    """
    parent = models.ForeignKey('self', default=0, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='父级',
                               limit_choices_to={'is_root': True})
    is_root = models.BooleanField(default=False, verbose_name='是否是一级分类')
    name = models.CharField(verbose_name='名称', unique=True, max_length=20)
    slug = models.CharField(verbose_name='slug', unique=True, blank=True, null=True, max_length=20)

    class Meta:
        verbose_name = '博客类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Article(BaseModel):
    """
    博客
    """
    STATUS_CHOICES = {
        'd': '草稿',
        'p': '已发布',
        'w': '撤销',
    }

    title = models.CharField('标题', unique=True, max_length=100)
    cover = models.CharField(u'封面', blank=True, max_length=255)
    slug = models.CharField('slug', unique=True, blank=True, null=True, max_length=20)
    content = MDTextField(u'正文', default='')
    views = models.PositiveIntegerField(u'热度', default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='博客类别')
    tags = TaggableManager(u'标签', blank=True)
    status = models.CharField(u'状态', max_length=1, choices=tuple(STATUS_CHOICES.items()), default='d')
    is_top = models.BooleanField(u'置顶', default=False)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', null=True)
    publish_time = models.DateTimeField(u'发布时间', null=True)
    allow_comments = models.BooleanField('开启评论', default=True)

    class Meta:
        verbose_name = '博客文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    # 后台管理状态加颜色。
    def colored_status(self):
        if self.status == 'd':
            color = 'grey'
        if self.status == 'p':
            color = 'green'
        if self.status == 'w':
            color = 'red'
        format_td = format_html(
            f'<span style="padding:2px;background-color:{color};color:white">{self.STATUS_CHOICES[self.status]}</span>')
        return format_td

    colored_status.short_description = "状态"

    def view_cover(self):
        return format_html("<img src='%s' height='200'/>" % self.cover)

    view_cover.short_description = '封面'
    view_cover.allow_tags = True

    def get_absolute_url(self):
        return reverse('blog:blog-detail', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = get_hash(self.title)[-10:]
        if not self.cover:
            self.cover = get_cover()
        modified = kwargs.pop("modified", True)
        if modified:
            self.update_time = timezone.now()

        if self.status in ['d', 'w']:
            self.publish_time = None

        if self.status == 'p' and not self.publish_time:
            self.publish_time = timezone.now()

        super(Article, self).save(*args, **kwargs)


class Comment(BaseModel):
    """
    博客评论
    """
    blog = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='博客')
    active = models.BooleanField(u'激活', default=True)
    name = models.CharField(u'姓名', max_length=20, default='佚名')
    email = models.EmailField(u'邮箱', max_length=20, default='pony@qq.com')
    content = models.TextField(u'内容')

    class Meta:
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content[:10]


class Friend(models.Model):
    """
    友情链接
    """
    name = models.CharField(u'名称', max_length=100, default='')
    link = models.URLField(u'链接', default='')
    cover = models.CharField(u'头像', blank=True, max_length=255)
    desc = models.TextField(u'描述', default='未添加描述')
    position = models.SmallIntegerField(u'位置', default=1)
    active = models.BooleanField(u'激活', default=True)

    class Meta:
        ordering = ['position']
        verbose_name = u'友情链接'
        verbose_name_plural = u'友情链接'

    def __str__(self):
        return self.name
