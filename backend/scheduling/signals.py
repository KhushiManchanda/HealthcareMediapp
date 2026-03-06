from django.db.models.signals import post_save
from django.dispatch import receiver
from scheduling.models import HealthEvent
from communication.models import Conversation, ConversationParticipant, Message
from health_assistant.models import ClinicalSummary

@receiver(post_save, sender=HealthEvent)
def create_chat_channel_for_appointment(sender, instance, created, **kwargs):
    """
    Automatically bridge scheduling to communication. 
    When an appointment is booked, a chat room is created between Patient and Doctor.
    The most recent AI Clinical Summary is appended to give the Doctor context.
    """
    if created and instance.event_type == 'appointment' and instance.doctor:
        # Strategy: find direct conversation between these two exact participants
        conversation = Conversation.objects.filter(
            conversation_type='direct',
            participants=instance.patient
        ).filter(
            participants=instance.doctor
        ).first()
        
        if not conversation:
            # Create a brand new direct channel
            conversation = Conversation.objects.create(
                clinic=instance.patient.clinic,
                conversation_type='direct',
                title=f"Chat: {instance.patient.user.get_full_name()} & Dr. {instance.doctor.user.get_last_name()}"
            )
            ConversationParticipant.objects.create(conversation=conversation, user=instance.patient)
            ConversationParticipant.objects.create(conversation=conversation, user=instance.doctor)
        
        # Fetch the latest ClinicalSummary for this patient to serve as context for the doctor
        latest_summary = ClinicalSummary.objects.filter(session__patient=instance.patient).order_by('created_at').last()
        
        if latest_summary:
            Message.objects.create(
                conversation=conversation,
                sender=None, # Sent as system message
                message_type='system',
                content=f"🩺 [AI Triage Summary Provided]\nComplaint: {latest_summary.chief_complaint}\nAnalysis: {latest_summary.ai_analysis}\nRecommendation: {latest_summary.recommended_action}"
            )
