from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from .models import TriageSession, TriageMessage, ClinicalSummary
from .serializers import TriageSessionSerializer, TriageMessageSerializer, ClinicalSummarySerializer

class TriageSessionViewSet(viewsets.ModelViewSet):
    queryset = TriageSession.objects.all()
    serializer_class = TriageSessionSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='message')
    def add_message(self, request, pk=None):
        """
        Custom endpoint handling live chatting with the Triage Assistant.
        When you POST here, it logs the user's message and triggers the LLM response.
        """
        session = self.get_object()
        content = request.data.get('content')

        if not content:
            return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 1. Save patient message
        TriageMessage.objects.create(session=session, sender='patient', content=content)
        
        # 2. [TODO] Trigger RAG (Retrieval-Augmented Generation) pipeline using OpenAI/Gemini here.
        # Placeholder for intelligent AI Assistant response
        ai_msg = TriageMessage.objects.create(
            session=session, 
            sender='ai', 
            content="I am securely analyzing your symptoms. Could you provide a bit more detail about when this started?"
        )

        return Response({"success": True, "ai_response": ai_msg.content})

class ClinicalSummaryViewSet(viewsets.ModelViewSet):
    queryset = ClinicalSummary.objects.all()
    serializer_class = ClinicalSummarySerializer
    permission_classes = [IsAuthenticated]
