from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Article, Comment


class ArticlesAdmin(admin.ModelAdmin):

    list_display = ('title', 'image_tag','text_article')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('image_tag',)


admin.site.site_header = 'ТНМК администрирование'
admin.site.register(Article, ArticlesAdmin)

class CommentAdmin(admin.ModelAdmin):

    list_display = ('author', 'body','created')
    def has_add_permission(self, request):
        return False

admin.site.register(Comment, CommentAdmin)
#admin.site.unregister(Group)
