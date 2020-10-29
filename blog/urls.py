"""blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from django.conf.urls.static import static

from myblog.views import IndexView, MySearchView
from blog import settings

# 修改标题
admin.AdminSite.site_header = settings.admin_title
admin.AdminSite.site_title = settings.admin_title

urlpatterns = [
    # 后台
    url(r'^admin/', admin.site.urls),
    # 首页
    url(r'^$', IndexView.as_view(), name='index'),
    # 搜索
    url(r'^search/', MySearchView(), name='haystack_search'),
    # 博客
    url(r'^blog/', include('myblog.urls')),
    # 添加静态文件的访问处理函数
    url(r'^static/(?P<path>.*)/$', serve, {'document_root': settings.STATIC_URL}),
    # markdown
    url(r'mdeditor/', include('mdeditor.urls')),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 配置全局404页面
hander404 = 'myblog.views.page_not_found'

# 配置全局505页面
hander505 = 'myblog.views.page_errors'
