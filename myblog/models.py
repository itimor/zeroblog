from django.db import models
from django.utils import timezone
from mdeditor.fields import MDTextField
import datetime


class Category(models.Model):
    """
    博客分类
    """
    name = models.CharField(verbose_name='博客类别', max_length=20)
    number = models.IntegerField(verbose_name='分类数目', default=1)

    class Meta:
        verbose_name = '博客类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    博客标签
    """
    name = models.CharField(verbose_name='博客标签', max_length=20)
    number = models.IntegerField(verbose_name='标签数目', default=1)

    class Meta:
        verbose_name = '博客标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Blog(models.Model):
    """
    博客
    """
    title = models.CharField(verbose_name='标题', max_length=100)
    content = MDTextField(verbose_name='正文', default='')
    excerpt = models.TextField(u'摘要', )
    create_time = models.DateTimeField(verbose_name='创建时间', default=timezone.now)
    modify_time = models.DateTimeField(verbose_name='修改时间', auto_now=True)
    click_nums = models.IntegerField(verbose_name='热度', default=0)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='博客类别')
    tag = models.ManyToManyField(Tag, verbose_name='博客标签')
    published = models.BooleanField(u'发布', default=True)
    is_top = models.BooleanField(u'置顶', default=False)
    publish_time = models.DateTimeField(u'发布时间', null=True)
    allow_comments = models.BooleanField('开启评论', default=True)

    class Meta:
        verbose_name = '博客文章'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        modified = kwargs.pop("modified", True)
        if modified:
            self.modify_time = datetime.datetime.utcnow()

        if self.published and not self.publish_time:
            self.publish_time = datetime.datetime.utcnow()

        # 生成摘要
        # 获取readmore位置
        readmore_index = self.content.find('<!--more-->')

        # 截取readmore前的字符串作为摘要并用markdown渲染
        self.excerpt = self.content[:readmore_index]

        super(Blog, self).save(*args, **kwargs)


class Comment(models.Model):
    """
    博客评论
    """
    name = models.CharField(verbose_name='姓名', max_length=20, default='佚名')
    content = models.CharField(verbose_name='内容', max_length=300)
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, verbose_name='博客')

    class Meta:
        verbose_name = '博客评论'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content[:10]


class Counts(models.Model):
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
