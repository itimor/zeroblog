from django.contrib import admin
from django.db import models
from mdeditor.widgets import MDEditorWidget
from blog.settings import admin_title
from myblog.models import Article, Category, Tag, Comment, Counts


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'click_nums', 'category', 'published', 'is_top', 'allow_comments', 'create_time', 'update_time']
    list_filter = ('published', 'is_top', 'publish_time', 'click_nums')
    fields = ('title', 'code', 'content', 'category', 'published', 'is_top', 'tags', 'allow_comments')
    # readonly_fields = ('click_nums',)
    exclude = ('publish_time',)
    search_fields = ('name', 'code')
    ordering = ('-create_time', 'published', 'is_top', 'publish_time')
    list_per_page = 20
    formfield_overrides = {
        models.TextField: {'widget': MDEditorWidget}
    }

    def save_model(self, request, obj, form, change):
        obj.save()
        # 统计博客数目
        blog_nums = Article.objects.filter(published=True).count()
        count_nums = Counts.objects.get(id=1)
        count_nums.blog_nums = blog_nums
        count_nums.save()
        # 博客分类数目统计
        obj_category = obj.category
        category_number = obj_category.article_set.count()
        obj_category.number = category_number
        obj_category.save()
        # 博客标签数目统计
        obj_tag_list = obj.tags.all()
        for obj_tag in obj_tag_list:
            tag_number = obj_tag.article_set.count()
            obj_tag.number = tag_number
            obj_tag.save()

    def delete_model(self, request, obj):
        # 统计博客数目
        blog_nums = Article.objects.count()
        count_nums = Counts.objects.get(id=1)
        count_nums.blog_nums = blog_nums - 1
        count_nums.save()
        # 博客分类数目统计
        obj_category = obj.category
        category_number = obj_category.blog_set.count()
        obj_category.number = category_number - 1
        obj_category.save()
        # 博客标签数目统计
        obj_tag_list = obj.tags.all()
        for obj_tag in obj_tag_list:
            tag_number = obj_tag.blog_set.count()
            obj_tag.number = tag_number - 1
            obj_tag.save()
        obj.delete()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'number', 'parent', 'is_root']

    def save_model(self, request, obj, form, change):
        obj.save()
        category_nums = Category.objects.count()
        count_nums = Counts.objects.get(id=1)
        count_nums.category_nums = category_nums
        count_nums.save()

    def delete_model(self, request, obj):
        obj.delete()
        category_nums = Category.objects.count()
        count_nums = Counts.objects.get(id=1)
        count_nums.category_nums = category_nums
        count_nums.save()


class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'number']

    def save_model(self, request, obj, form, change):
        obj.save()
        tag_nums = Tag.objects.count()
        count_nums = Counts.objects.get(id=1)
        count_nums.tag_nums = tag_nums
        count_nums.save()

    def delete_model(self, request, obj):
        obj.delete()
        tag_nums = Tag.objects.count()
        count_nums = Counts.objects.get(id=1)
        count_nums.tag_nums = tag_nums
        count_nums.save()


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'blog', 'content', 'create_time']


class CountsAdmin(admin.ModelAdmin):
    list_display = ['blog_nums', 'category_nums', 'tag_nums', 'visit_nums']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Counts, CountsAdmin)

# 修改标题
admin.AdminSite.site_header = admin_title
admin.AdminSite.site_title = admin_title
