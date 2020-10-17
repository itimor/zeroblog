# -*- coding: utf-8 -*-
# author: itimor

from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from myblog.models import *


class Command(BaseCommand):
    def handle(self, *args, **options):
        try:
            self.stdout.write(self.style.SUCCESS('############ 初始化管理员 ###########'))
            User.objects.create(username='admin', password=make_password("123456"), email='itimor@126.com',
                                is_staff=True, is_superuser=True)
        except:
            raise CommandError('初始化管理员失败')

        self.stdout.write(self.style.SUCCESS('############ 初始化博客分类 ###########'))
        category = Category.objects.create(parent=None, is_root=True, name='其他', code='other', number=1)

        self.stdout.write(self.style.SUCCESS('############ 初始化博客标签 ###########'))
        tag = Tag.objects.create(name='其他', code='other', number=1)

        self.stdout.write(self.style.SUCCESS('############ 初始化博客文章 ###########'))
        content = """# h1 标题
## h2 标题
### h3 标题
#### h4 标题

## 水平线
___
---
***

<!--more-->
## 文本样式

**This is bold text**

__This is bold text__

*This is italic text*

_This is italic text_

~~Strikethrough~~


## 列表

无序

+ Create a list by starting a line with `+`, `-`, or `*`
+ Sub-lists are made by indenting 2 spaces:
  - Marker character change forces new list start:
    * Ac tristique libero volutpat at
    + Facilisis in pretium nisl aliquet
    - Nulla volutpat aliquam velit
+ Very easy!

有序

1. Lorem ipsum dolor sit amet
2. Consectetur adipiscing elit
3. Integer molestie lorem at massa


1. You can use sequential numbers...
1. ...or keep all the numbers as `1.`

Start numbering with offset:

57. foo
1. bar


## 代码

Inline `code`

Indented code

    // Some comments
    line 1 of code
    line 2 of code
    line 3 of code


Block code "fences"

```
Sample text here...
```

Syntax highlighting

``` js
var foo = function (bar) {
  return bar++;
};

console.log(foo(5));
```"""
        blog = Article.objects.create(title='这是你的第一篇markdown文章', code='16886688', content=content, published=True,
                                   category=category)
        blog.tags.add(tag)

        self.stdout.write(self.style.SUCCESS('############ 初始化博客统计 ###########'))
        Counts.objects.create(blog_nums=1, category_nums=1, tag_nums=1, visit_nums=0)

        self.stdout.write(self.style.SUCCESS('初始化完成'))
