from django.contrib import admin

from .models import Article, Type, Category, ArticleComment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','content')


class ArticleCommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'object_pk', 'short_comment')

    def short_comment(self, obj):
        return '%s...' % obj.comment[:50]
    short_comment.short_description = 'Comment'

admin.site.register(Type)
admin.site.register(Category)
admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleComment, ArticleCommentAdmin)
