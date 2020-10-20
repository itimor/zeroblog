from django.contrib import admin
from spider.models import SpiderInfo


class SpiderInfoAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'keyword', 'base_url', 'memo']


admin.site.register(SpiderInfo, SpiderInfoAdmin)
