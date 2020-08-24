from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):

    list_display = ('first_name', 'last_name','bio','birth_date')
    prepopulated_fields = {"slug": ("first_name",'last_name')}
    #readonly_fields = ('image_tag',)


admin.site.site_header = 'ТНМК администрирование'
admin.site.register(Profile, ProfileAdmin)

