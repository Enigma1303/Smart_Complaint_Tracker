from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Complaint
from .serializers import ComplaintSerializer,ComplaintUpdateSerializer

class ComplaintViewSet(viewsets.ModelViewSet):

    permission_classes=[IsAuthenticated]
    queryset=Complaint.objects.all()

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return ComplaintUpdateSerializer
        else:
            return ComplaintSerializer

    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)
