from django.contrib import admin
from .models import Message, Chat


class MessageAdmin(admin.ModelAdmin):

    #def has_add_permission(self, request):
        #return False
    pass


admin.site.register(Message, MessageAdmin)


class ChatAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("group_name", 'creater')}
    pass


admin.site.register(Chat, ChatAdmin)
