from django.contrib import admin
from blog.settings import admin_title
from myblog.models import Article, Category, Comment, Counts


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'click_nums', 'category', 'published', 'is_top', 'allow_comments', 'create_time',
                    'update_time']
    list_filter = ('published', 'is_top', 'publish_time', 'click_nums')
    fields = ('title', 'code', 'content', 'category', 'published', 'is_top', 'tags', 'allow_comments', 'source')
    readonly_fields = ('source',)
    exclude = ('publish_time',)
    search_fields = ('title', 'code')
    ordering = ('-create_time', 'published', 'is_top', 'publish_time')
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        obj.save()
        # 统计博客数目
        blog_nums = Article.objects.filter(published=True).count()
        count_nums = Counts.objects.get(id=1)
        count_nums.blog_nums = blog_nums
        count_nums.save()

    def delete_model(self, request, obj):
        # 统计博客数目
        blog_nums = Article.objects.count()
        count_nums = Counts.objects.get(id=1)
        count_nums.blog_nums = blog_nums - 1
        count_nums.save()
        obj.delete()


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'number', 'parent', 'is_root']
    search_fields = ('name', 'code')

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


class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'blog', 'content', 'create_time']
    search_fields = ('blog', 'content')


class CountsAdmin(admin.ModelAdmin):
    list_display = ['blog_nums', 'category_nums', 'tag_nums', 'visit_nums']


admin.site.register(Article, ArticleAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Counts, CountsAdmin)

# 修改标题
admin.AdminSite.site_header = admin_title
admin.AdminSite.site_title = admin_title
