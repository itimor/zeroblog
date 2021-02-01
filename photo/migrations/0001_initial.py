# Generated by Django 3.1.5 on 2021-02-01 11:00

from django.db import migrations, models
import django.db.models.deletion
import utils.storage


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PhotoGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150, unique=True, verbose_name='标题')),
                ('cover', models.CharField(blank=True, max_length=255, verbose_name='封面')),
                ('desc', models.TextField(verbose_name='描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('active', models.BooleanField(default=True, verbose_name='开启')),
            ],
            options={
                'verbose_name': '相册',
                'verbose_name_plural': '相册',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('photo', models.ImageField(upload_to=utils.storage.PathAndRename('photo'), verbose_name='照片')),
                ('desc', models.TextField(blank=True, null=True, verbose_name='描述')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('group', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='photo.photogroup')),
            ],
            options={
                'verbose_name': '照片',
                'verbose_name_plural': '照片',
            },
        ),
    ]
