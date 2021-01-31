# -*- coding: utf-8 -*-
# author: itimor

from django.db import models
from django.utils.html import format_html

from utils.storage import PathAndRename
from utils.index import get_cover


class PhotoGroup(models.Model):
    name = models.CharField(u'标题', max_length=150, unique=True)
    cover = models.CharField(u'封面', blank=True, max_length=255)
    desc = models.TextField(u'描述', )
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)
    active = models.BooleanField(u'开启', default=True)

    class Meta:
        verbose_name = u'相册'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def view_cover(self):
        return format_html("<img src='%s' height='200'/>" % self.cover)

    def save(self, *args, **kwargs):
        if not self.cover:
            self.cover = get_cover()
        super(PhotoGroup, self).save(*args, **kwargs)


class Photo(models.Model):
    photo = models.ImageField(upload_to=PathAndRename("photo"), verbose_name=u'照片')
    desc = models.TextField(null=True, blank=True, verbose_name=u'描述')
    group = models.ForeignKey('PhotoGroup', on_delete=models.CASCADE, blank=True)
    create_time = models.DateTimeField(u'创建时间', auto_now_add=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True)

    class Meta:
        verbose_name = u'照片'
        verbose_name_plural = verbose_name

    def view_img(self):
        return format_html("<img src='/res/%s' height='200'/>" % self.photo)

    view_img.short_description = '预览'
    view_img.allow_tags = True
