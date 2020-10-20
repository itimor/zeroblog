# -*- coding: utf-8 -*-
# author: itimor


def gen_markdown_table(header, header_code, data):
    n = len(header)
    lines = []
    ## 表头部分
    lines += ["{}".format(' | '.join(header))]

    ## 分割线
    line = ''
    for i in range(n):
        line += "{}".format(' -- |')
    lines += [line.rstrip(' | ')]

    ## 数据部分
    for d in data:
        line = []
        for i in header_code:
            line += [str(d[i])]
        lines += [' | '.join(line)]
    table = '\n'.join(lines)
    return table


if __name__ == '__main__':
    header = ["名称", "性别", "电话"]
    header_code = ["name", "sex", "tel"]
    data = [
        {'name': 'aa', 'sex': 1, 'tel': 11},
        {'name': 'bb', 'sex': 2, 'tel': 22},
        {'name': 'cc', 'sex': 3, 'tel': 33},
    ]
    p = gen_markdown_table(header, header_code, data)
    print(p)

