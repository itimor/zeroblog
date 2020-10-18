# Generated by Django 3.1.2 on 2020-10-18 07:12

from django.db import migrations, models
import django.db.models.deletion
import mdeditor.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
                ('title', models.CharField(max_length=100, verbose_name='标题')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='code')),
                ('content', mdeditor.fields.MDTextField(default='', verbose_name='正文')),
                ('click_nums', models.IntegerField(default=0, verbose_name='热度')),
                ('published', models.BooleanField(default=True, verbose_name='发布')),
                ('is_top', models.BooleanField(default=False, verbose_name='置顶')),
                ('publish_time', models.DateTimeField(null=True, verbose_name='发布时间')),
                ('allow_comments', models.BooleanField(default=True, verbose_name='开启评论')),
                ('source', models.CharField(blank=True, max_length=254, verbose_name='来源地址')),
            ],
            options={
                'verbose_name': '博客文章',
                'verbose_name_plural': '博客文章',
            },
        ),
        migrations.CreateModel(
            name='Counts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
                ('blog_nums', models.IntegerField(default=0, verbose_name='博客数目')),
                ('category_nums', models.IntegerField(default=0, verbose_name='分类数目')),
                ('tag_nums', models.IntegerField(default=0, verbose_name='标签数目')),
                ('visit_nums', models.IntegerField(default=0, verbose_name='网站访问量')),
            ],
            options={
                'verbose_name': '数目统计',
                'verbose_name_plural': '数目统计',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='博客标签')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='code')),
                ('number', models.IntegerField(default=1, verbose_name='标签数目')),
            ],
            options={
                'verbose_name': '博客标签',
                'verbose_name_plural': '博客标签',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
                ('name', models.CharField(default='佚名', max_length=20, verbose_name='姓名')),
                ('content', models.CharField(max_length=300, verbose_name='内容')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myblog.article', verbose_name='博客')),
            ],
            options={
                'verbose_name': '博客评论',
                'verbose_name_plural': '博客评论',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('memo', models.TextField(blank=True, verbose_name='备注')),
                ('is_root', models.BooleanField(default=False, verbose_name='是否是一级分类')),
                ('name', models.CharField(max_length=20, unique=True, verbose_name='博客类别')),
                ('code', models.CharField(max_length=20, unique=True, verbose_name='code')),
                ('number', models.IntegerField(default=1, verbose_name='分类数目')),
                ('parent', models.ForeignKey(blank=True, default=0, limit_choices_to={'is_root': True}, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myblog.category', verbose_name='父级')),
            ],
            options={
                'verbose_name': '博客类别',
                'verbose_name_plural': '博客类别',
            },
        ),
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myblog.category', verbose_name='博客类别'),
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(to='myblog.Tag', verbose_name='博客标签'),
        ),
    ]
