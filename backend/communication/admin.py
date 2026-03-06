from django.contrib import admin
from .models import Announcement, Conversation, ConversationParticipant, Message, Notification, NotificationPreference

admin.site.register(Announcement)
admin.site.register(Conversation)
admin.site.register(ConversationParticipant)
admin.site.register(Message)
admin.site.register(Notification)
admin.site.register(NotificationPreference)
