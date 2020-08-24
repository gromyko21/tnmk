from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Article


class ArticlesAdmin(admin.ModelAdmin):

    list_display = ('title', 'image_tag','text_article')
    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ('image_tag',)


admin.site.site_header = 'ТНМК администрирование'
admin.site.register(Article, ArticlesAdmin)
#admin.site.unregister(Group)
