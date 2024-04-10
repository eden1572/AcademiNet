
from django.contrib import admin
from .models import Message,Notification

class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject',  'receiver', 'created_at')
    search_fields = ('subject', 'sender__username', 'receiver__username')


class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'timestamp', 'read')
    list_filter = ('user', 'timestamp', 'read')
    search_fields = ('message', 'user__username')
    readonly_fields = ('timestamp',)  # Mark timestamp as read-only


admin.site.register(Notification, NotificationAdmin)
admin.site.register(Message,MessageAdmin)