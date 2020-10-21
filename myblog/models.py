from django.db import models
from mdeditor.fields import MDTextField
from django.utils import timezone

from utils.db import BaseModel
from utils.index import get_hash


class Category(BaseModel):
    """
    博客分类
    """
    parent = models.ForeignKey('self', default=0, null=True, blank=True, on_delete=models.SET_NULL, verbose_name='父级',
                               limit_choices_to={'is_root': True})
    is_root = models.BooleanField(default=False, verbose_name='是否是一级分类')
    name = models.CharField(verbose_name='博客类别', unique=True, max_length=20)
    code = models.CharField(verbose_name='code', unique=True, max_length=20)
    number = models.IntegerField(verbose_name='分类数目', default=1)

    class Meta:
        verbose_name = '博客类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Article(BaseModel):
    """
    博客
    """
    title = models.CharField(verbose_name='标题', unique=True, max_length=100)
    code = models.CharField(verbose_name='code', unique=True, blank=True, null=True, max_length=20)
    content = MDTextField(verbose_name='正文', default='')
    click_nums = models.IntegerField(verbose_name='热度', default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='博客类别')
    tags = models.CharField(verbose_name='标签', default="其他", max_length=100)
    published = models.BooleanField(u'发布', default=True)
    is_top = models.BooleanField(u'置顶', default=False)
    publish_time = models.DateTimeField(u'发布时间', null=True)
    allow_comments = models.BooleanField('开启评论', default=True)
    source = models.CharField(verbose_name='来源地址', max_length=254, blank=True)

    class Meta:
        verbose_name = '博客文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.code = get_hash(self.title, str(self.id))[-10:]
        modified = kwargs.pop("modified", True)
        if modified:
            self.update_time = timezone.now()

        if self.published and not self.publish_time:
            self.publish_time = timezone.now()

        super(Article, self).save(*args, **kwargs)


class Comment(BaseModel):
    """
    博客评论
    """
    name = models.CharField(verbose_name='姓名', max_length=20, default='佚名')
    content = models.CharField(verbose_name='内容', max_length=300)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='博客')

    class Meta:
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content[:10]


class Counts(BaseModel):
    """
    统计博客、分类和标签的数目
    """
    blog_nums = models.IntegerField(verbose_name='博客数目', default=0)
    category_nums = models.IntegerField(verbose_name='分类数目', default=0)
    tag_nums = models.IntegerField(verbose_name='标签数目', default=0)
    visit_nums = models.IntegerField(verbose_name='网站访问量', default=0)

    class Meta:
        verbose_name = '数目统计'
        verbose_name_plural = verbose_name
