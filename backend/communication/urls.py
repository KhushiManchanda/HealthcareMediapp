from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AnnouncementViewSet, AnnouncementReadViewSet, ConversationViewSet,
    ConversationParticipantViewSet, MessageViewSet, NotificationViewSet,
    NotificationPreferenceViewSet, BlockedUserViewSet
)

router = DefaultRouter()
router.register(r'announcements', AnnouncementViewSet, basename='announcements')
router.register(r'announcement-reads', AnnouncementReadViewSet, basename='announcement-reads')
router.register(r'conversations', ConversationViewSet, basename='conversations')
router.register(r'participants', ConversationParticipantViewSet, basename='participants')
router.register(r'messages', MessageViewSet, basename='messages')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'preferences', NotificationPreferenceViewSet, basename='preferences')
router.register(r'blocked-users', BlockedUserViewSet, basename='blocked-users')

urlpatterns = [
    path('', include(router.urls)),
]
