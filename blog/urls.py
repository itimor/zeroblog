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

from blog import settings

# 修改标题
admin.AdminSite.site_header = settings.admin_title
admin.AdminSite.site_title = settings.admin_title

urlpatterns = [
    # 后台
    url(r'^admin/', admin.site.urls),
    # 博客
    url(r'^', include('myblog.urls')),
    # 相册
    url(r'^photo/', include('photo.urls')),
    # 添加静态文件的访问处理函数
    url(r'^statics/(?P<path>.*)/$', serve, {'document_root': settings.STATIC_ROOT}),
    # markdown
    url(r'mdeditor/', include('mdeditor.urls')),
]

if settings.DEBUG:
    # static files (images, css, javascript, etc.)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += url(r'^statics/(?P<path>.*)/$', serve, {'document_root': settings.STATIC_URL}),
else:
    urlpatterns += url(r'^statics/(?P<path>.*)/$', serve, {'document_root': settings.STATIC_ROOT}),

from myblog.error_views import bad_request, permission_denied, page_not_found, server_error

# 定义错误跳转页面
handler400 = bad_request
handler403 = permission_denied
handler404 = page_not_found
handler500 = server_error
