# -*- coding: utf-8 -*-
# author: itimor

from django.contrib import admin
from photo.models import Photo, PhotoGroup


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    model = Photo
    list_display = ['group', 'photo', 'desc']
    fields = ['group', 'photo', ('desc', 'view_img')]
    readonly_fields = ['view_img']
    exclude = ['view_img']


class PhotoInlineAdmin(admin.StackedInline):
    model = Photo
    fields = ['photo', ('desc', 'view_img')]
    readonly_fields = ['view_img']
    exclude = ['view_img']


@admin.register(PhotoGroup)
class PhotoGroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'create_time', 'update_time', 'active']
    list_filter = ['active', 'create_time', 'update_time']
    fields = ['name', 'active', ('desc', 'view_cover')]
    readonly_fields = ['view_cover']
    exclude = ['view_cover']
    inlines = [PhotoInlineAdmin]
