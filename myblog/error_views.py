# -*- coding: utf-8 -*-
# author: itimor

from django.shortcuts import render

template_name = 'error.html'


# 自定义错误页面
def bad_request(request, exception):
    data = {"code": 400, "msg": "发生了一个未知的错误"}
    return render(request, template_name, data)


def permission_denied(request, exception):
    data = {"code": 403, "msg": "这不是你该来的地方"}
    return render(request, template_name, data)


def page_not_found(request, exception):
    data = {"code": 404, "msg": "你进了一个未知的地方"}
    return render(request, template_name, data)


def server_error(request):
    data = {"code": 500, "msg": "代码出bug了"}
    return render(request, template_name, data)