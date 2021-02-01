# -*- coding: utf-8 -*-
# author: itimor

import requests
import hashlib
from hashlib import sha1


def get_hash(str, salt=None):  # salt 盐
    '''取一个字符串的hash值'''
    # 提高字符串的复杂度
    str = '!@#$%' + str + '&^**('
    if salt:
        str = str + salt
    # 取str　hash值
    sh = sha1()
    sh.update(str.encode('utf-8'))
    return sh.hexdigest()


def get_cover(w=600, h=800):
    url = f'https://source.unsplash.com/random/{w}x{h}'
    session = requests.Session()
    r = session.get(url)
    return r.url


def gen_md5(str):
    md5 = hashlib.md5()
    # 实例化md5加密方法
    md5.update(str.encode())
    # 进行加密，python2可以给字符串加密，python3只能给字节加密
    result = md5.hexdigest()
    return result


def gen_markdown_table(header, header_code, data):
    n = len(header)
    lines = []
    # 表头部分
    lines += ["{}".format(' | '.join(header))]

    # 分割线
    line = ''
    for i in range(n):
        line += "{}".format(' -- |')
    lines += [line.rstrip(' | ')]

    # 数据部分
    for d in data:
        line = []
        for i in header_code:
            line += [str(d[i])]
        lines += [' | '.join(line)]
    table = '\n'.join(lines)
    return table


if __name__ == '__main__':
    # header = ["名称", "性别", "电话"]
    # header_code = ["name", "sex", "tel"]
    # data = [
    #     {'name': 'aa', 'sex': 1, 'tel': 11},
    #     {'name': 'bb', 'sex': 2, 'tel': 22},
    #     {'name': 'cc', 'sex': 3, 'tel': 33},
    # ]
    # p = gen_markdown_table(header, header_code, data)
    p = get_cover()
    print(p)
