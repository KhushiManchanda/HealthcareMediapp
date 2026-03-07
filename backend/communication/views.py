from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import (
    Announcement, AnnouncementRead, Conversation,
    ConversationParticipant, Message, Notification,
    NotificationPreference, BlockedUser
)
from .serializers import (
    AnnouncementSerializer, AnnouncementReadSerializer, ConversationSerializer,
    ConversationParticipantSerializer, MessageSerializer, NotificationSerializer,
    NotificationPreferenceSerializer, BlockedUserSerializer
)

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    permission_classes = [IsAuthenticated]

class AnnouncementReadViewSet(viewsets.ModelViewSet):
    queryset = AnnouncementRead.objects.all()
    serializer_class = AnnouncementReadSerializer
    permission_classes = [IsAuthenticated]

class ConversationViewSet(viewsets.ModelViewSet):
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]

class ConversationParticipantViewSet(viewsets.ModelViewSet):
    queryset = ConversationParticipant.objects.all()
    serializer_class = ConversationParticipantSerializer
    permission_classes = [IsAuthenticated]

class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

class NotificationPreferenceViewSet(viewsets.ModelViewSet):
    queryset = NotificationPreference.objects.all()
    serializer_class = NotificationPreferenceSerializer
    permission_classes = [IsAuthenticated]

class BlockedUserViewSet(viewsets.ModelViewSet):
    queryset = BlockedUser.objects.all()
    serializer_class = BlockedUserSerializer
    permission_classes = [IsAuthenticated]