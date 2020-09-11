from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):

    #def has_add_permission(self, request):
        #return False
    pass


admin.site.register(Message, MessageAdmin)


# class ChatAdmin(admin.ModelAdmin):
#   #  prepopulated_fields = {"slug": ("members", 'members')}
#     pass
#
#
# admin.site.register(Chat, ChatAdmin)
