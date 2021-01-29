from django.contrib import admin
from blog.settings import admin_title
from myblog.models import Article, Category, Tag, Comment, TagManager
from django.utils import timezone


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'views', 'category', 'colored_status', 'is_top', 'allow_comments', 'create_time',
                    'publish_time']
    list_filter = ['status', 'is_top', 'publish_time', 'views']
    fieldsets = (
        ("基础信息", {'fields': ['title', 'slug', 'tags']}),
        ("状态", {'fields': ['status', 'category', 'is_top', 'allow_comments']}),
        ("内容", {'fields': ['content']})
    )
    readonly_fields = ['slug']
    exclude = ['publish_time']
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
    list_display = ['name', 'slug', 'number', 'parent', 'is_root']
    search_fields = ['name', 'slug']


class TagManagerInline(admin.StackedInline):
    model = TagManager


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    inlines = [TagManagerInline]
    list_display = ["name", "slug"]
    ordering = ["name", "slug"]
    search_fields = ["name"]
    prepopulated_fields = {"slug": ["name"]}


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'blog', 'content', 'create_time']
    search_fields = ['blog', 'content']
