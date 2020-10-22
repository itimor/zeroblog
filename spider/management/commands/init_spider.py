# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from myblog.models import *
from spider.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        top = Category.objects.create(parent=None, is_root=True, name='爬虫', code='spider')

        self.stdout.write(self.style.SUCCESS('############ 初始化爬虫信息 ###########'))
        obj = SpiderInfo.objects.create(name='零点财经', code='zcaijing', keyword='', base_url='https://www.zcaijing.com')
        Category.objects.create(parent=top, is_root=False, name=obj.name, code=obj.code)

        obj = SpiderInfo.objects.create(name='巨潮资讯', code='cninfo', keyword='新能源 汽车',
                                        base_url='http://www.cninfo.com.cn')
        Category.objects.create(parent=top, is_root=False, name=obj.name, code=obj.code)

        self.stdout.write(self.style.SUCCESS('初始化完成'))
