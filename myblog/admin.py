from django.contrib import admin
from blog.settings import admin_title
from myblog.models import Article, Category, Comment, Counts
from django.utils import timezone


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'click_nums', 'category', 'colored_status', 'is_top', 'allow_comments', 'create_time', 'publish_time']
    list_filter = ['status', 'is_top', 'publish_time', 'click_nums']
    fieldsets = (
        ("基础信息", {'fields': ['title', 'code', 'tags']}),
        ("状态", {'fields': ['status', 'category', 'is_top', 'allow_comments']}),
        ("内容", {'fields': ['content']})
    )
    readonly_fields = ['code']
    exclude = ['publish_time']
    search_fields = ['title', 'code']
    ordering = ['-create_time', 'status', 'is_top', 'publish_time']
    list_per_page = 20
    actions = ['make_draft', 'make_published', 'make_withdrawn', 'make_top', 'make_commit']

    def save_model(self, request, obj, form, change):
        obj.save()
        # 统计博客数目
        blog_nums = Article.objects.filter(status='p').count()
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

    def make_draft(self, request, queryset):
        queryset.update(status='d')
        queryset.update(publish_time=None)

    def make_published(self, request, queryset):
        queryset.update(status='p')
        queryset.update(publish_time=timezone.now())

    def make_withdrawn(self, request, queryset):
        queryset.update(status='w')
        queryset.update(publish_time=None)

    def make_top(self, request, queryset):
        queryset.update(is_top=True)

    def make_commit(self, request, queryset):
        queryset.update(allow_comments=True)

    make_draft.short_description = "草稿"
    make_published.short_description = "发布"
    make_withdrawn.short_description = "撤销"
    make_top.short_description = "置顶"
    make_commit.short_description = "开启评论"


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
