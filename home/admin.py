from django.contrib import admin
from .models import Article, Comment, Question, Answer, AnswerUser


class AnswerInline(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'date_published', 'is_active')
    fields = ['is_active', 'title', 'article_id']
    inlines = [AnswerInline]


class ArticlesAdmin(admin.ModelAdmin):
    '''
    Записи на главной странице
    '''
    list_display = ('title', 'text_article')
    prepopulated_fields = {"slug": ("title",)}


admin.site.register(Article, ArticlesAdmin)
admin.site.register(AnswerUser)


class CommentAdmin(admin.ModelAdmin):
    '''
    Комментарии к записям на главной странице
    '''
    list_display = ('author', 'body','created')

    def has_add_permission(self, request):
        return False


admin.site.register(Comment, CommentAdmin)

admin.site.register(Question, QuestionAdmin)
