import uuid
from django.conf import settings
from django.db import models
from django.utils import timezone
from users.models import Clinic, ClinicUser

# =============================================================================
# Announcements (Health Advisories)
# =============================================================================

class Announcement(models.Model):
    """
    Health Advisories and Clinic-wide Announcements.
    """
    AUDIENCE_CHOICES = (
        ('all', 'All Users'),
        ('patients', 'Patients Only'),
        ('doctors', 'Doctors Only'),
        ('staff', 'Staff Only'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='announcements')

    title = models.CharField(max_length=255)
    content = models.TextField()

    target_audience = models.CharField(max_length=20, choices=AUDIENCE_CHOICES, default='all')
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')

    publish_at = models.DateTimeField(default=timezone.now)
    expire_at = models.DateTimeField(null=True, blank=True)

    attachment = models.FileField(upload_to='announcements/%Y/%m/', null=True, blank=True)
    attachment_name = models.CharField(max_length=255, blank=True)

    is_published = models.BooleanField(default=True)
    is_pinned = models.BooleanField(default=False)

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_pinned', '-publish_at']

    def __str__(self):
        return f"{self.clinic.name}: {self.title}"

class AnnouncementRead(models.Model):
    """Tracks which users have read an announcement."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    announcement = models.ForeignKey(Announcement, on_delete=models.CASCADE, related_name='reads')
    user = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='read_announcements')
    read_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('announcement', 'user')

# =============================================================================
# Messaging System
# =============================================================================

class Conversation(models.Model):
    """
    A conversation between users. Supports Direct Messages between Doctor & Patient.
    """
    CONVERSATION_TYPES = (
        ('direct', 'Direct Message'),
        ('group', 'Group Conversation'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    clinic = models.ForeignKey(Clinic, on_delete=models.CASCADE, related_name='conversations')
    conversation_type = models.CharField(max_length=20, choices=CONVERSATION_TYPES, default='direct')

    title = models.CharField(max_length=255, blank=True)

    participants = models.ManyToManyField(ClinicUser, through='ConversationParticipant', related_name='conversations')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    last_message_at = models.DateTimeField(null=True, blank=True)
    last_message_preview = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ['-last_message_at', '-created_at']

    def __str__(self):
        return self.title if self.title else f"Conversation #{self.pk}"

    def update_last_message(self, message):
        self.last_message_at = message.created_at
        self.last_message_preview = message.content[:100] if message.content else '[Attachment]'
        self.save(update_fields=['last_message_at', 'last_message_preview', 'updated_at'])

class ConversationParticipant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='conversation_participants')
    user = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='conversation_participations')

    last_read_at = models.DateTimeField(null=True, blank=True)
    unread_count = models.PositiveIntegerField(default=0)
    is_muted = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)

    joined_at = models.DateTimeField(auto_now_add=True)
    left_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('conversation', 'user')

class Message(models.Model):
    MESSAGE_TYPES = (
        ('text', 'Text'),
        ('file', 'File'),
        ('image', 'Image'),
        ('voice', 'Voice Message'),
        ('system', 'System Message'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(ClinicUser, on_delete=models.SET_NULL, null=True, related_name='sent_messages')

    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPES, default='text')
    content = models.TextField(blank=True)

    attachment = models.FileField(upload_to='messages/%Y/%m/', null=True, blank=True)
    attachment_name = models.CharField(max_length=255, blank=True)

    reply_to = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='replies')

    is_edited = models.BooleanField(default=False)
    edited_at = models.DateTimeField(null=True, blank=True)
    is_deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        if is_new and not self.is_deleted:
            self.conversation.update_last_message(self)
            ConversationParticipant.objects.filter(
                conversation=self.conversation
            ).exclude(
                user=self.sender
            ).update(
                unread_count=models.F('unread_count') + 1
            )

# =============================================================================
# Notifications
# =============================================================================

class Notification(models.Model):
    NOTIFICATION_TYPES = (
        ('announcement', 'New Announcement'),
        ('message', 'New Message'),
        ('appointment', 'Appointment Reminder'),
        ('medicine', 'Medicine Reminder'),
        ('report', 'Report Ready'),
        ('system', 'System'),
    )

    PRIORITY_CHOICES = (
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    recipient = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='normal')

    title = models.CharField(max_length=255)
    message = models.TextField()

    related_object_type = models.CharField(max_length=50, blank=True)
    related_object_id = models.UUIDField(null=True, blank=True)

    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class NotificationPreference(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(ClinicUser, on_delete=models.CASCADE, related_name='notification_preferences')

    email_appointments = models.BooleanField(default=True)
    push_appointments = models.BooleanField(default=True)
    push_messages = models.BooleanField(default=True)
    push_medicines = models.BooleanField(default=True)

    updated_at = models.DateTimeField(auto_now=True)

class BlockedUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    blocker = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='blocked_users')
    blocked_user = models.ForeignKey(ClinicUser, on_delete=models.CASCADE, related_name='blocked_by_users')
    reason = models.CharField(max_length=50, blank=True, default='other')
    blocked_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blocker', 'blocked_user')

