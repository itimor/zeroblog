from django.db import models

from utils.db import BaseModel


class SpiderInfo(BaseModel):
    """
    爬虫信息
    """
    name = models.CharField(verbose_name='名称', unique=True, max_length=20)
    code = models.CharField(verbose_name='code', unique=True, max_length=20)
    keyword = models.CharField(verbose_name='关键字', blank=True, max_length=200, help_text='多个关键字用空格分开')
    base_url = models.CharField(verbose_name='域名', unique=True, max_length=100)

    class Meta:
        verbose_name = '爬虫信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

