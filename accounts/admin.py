from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile,Post


class ProfileAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name','image_tag','position','bio','birth_date')
    prepopulated_fields = {"slug": ("first_name",'last_name')}
    readonly_fields = ('image_tag',)
    def has_add_permission(self, request):
        return False


admin.site.site_header = 'ТНМК администрирование'
admin.site.register(Profile, ProfileAdmin)

class PostAdmin(admin.ModelAdmin):

    list_display = ('author','image_tag', 'text','datetime')
    readonly_fields = ('image_tag',)
    def has_add_permission(self, request):
        return False

admin.site.register(Post, PostAdmin)
