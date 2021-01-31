# -*- coding: utf-8 -*-
# author: itimor

from django.conf.urls import url
from photo.views import PhotoGroupView, PhotoView, UploadView

app_name = 'photo'
urlpatterns = [
    url(r'^$', PhotoGroupView.as_view(), name="photogroup"),
    url(r'^photogroup/(?P<group_id>\d+)/$', PhotoView.as_view(), name="photogroup-detail"),
    url(r'^upload/$', UploadView.as_view(), name="upload"),
]