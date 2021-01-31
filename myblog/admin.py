from django.contrib import admin
from blog.settings import admin_title
from myblog.models import Article, Category, Comment, Friend
from django.utils import timezone


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'views', 'category', 'colored_status', 'is_top', 'allow_comments', 'create_time',
                    'publish_time']
    list_filter = ['status', 'is_top', 'publish_time', 'views']
    fieldsets = (
        ("基础", {'fields': ['title', 'view_cover']}),
        ("状态", {'fields': [('tags', 'slug'), ('status', 'is_top'), ('category', 'allow_comments')]}),
        ("内容", {'fields': ['content']})
    )
    readonly_fields = ['slug', 'view_cover']
    exclude = ['publish_time', 'view_cover']
    search_fields = ['title', 'slug']
    ordering = ['-create_time', 'status', 'is_top', 'publish_time']
    list_per_page = 20
    actions = ['make_draft', 'make_published', 'make_withdrawn', 'make_top', 'make_commit']

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


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'is_root']
    search_fields = ['name', 'slug']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'blog', 'active', 'create_time']
    fields = ['name', 'email', 'active', 'blog', 'content']
    search_fields = ['name', 'blog', 'content']


@admin.register(Friend)
class FriendAdmin(admin.ModelAdmin):
    list_display = ('name', 'link', 'position', 'active')