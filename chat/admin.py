from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):

    def has_add_permission(self, request):
        return False


admin.site.register(Message, MessageAdmin)
