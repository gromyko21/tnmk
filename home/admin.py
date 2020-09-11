from django.contrib import admin
from .models import Article, Comment


class ArticlesAdmin(admin.ModelAdmin):
    '''
    Записи на главной странице
    '''
    list_display = ('title','text_article')
    prepopulated_fields = {"slug": ("title",)}
    #readonly_fields = ('image_tag',)


admin.site.register(Article, ArticlesAdmin)


class CommentAdmin(admin.ModelAdmin):
    '''
    Комментарии к записям на главной странице
    '''
    list_display = ('author', 'body','created')
    def has_add_permission(self, request):
        return False


admin.site.register(Comment, CommentAdmin)

