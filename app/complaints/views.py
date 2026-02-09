from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter

from .models import Complaint
from .serializers import ComplaintSerializer,ComplaintUpdateSerializer

@extend_schema(
    parameters=[
        OpenApiParameter(
            name="status",
            description="Filter by complaint status (OPEN, IN_PROGRESS, RESOLVED)",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="category",
            description="Filter by complaint category (ROAD, WATER, ELECTRICITY)",
            required=False,
            type=str,
        ),
        OpenApiParameter(
            name="userId",
            description="Set ID  to get complaints created by the logged-in user",
            required=False,
            type=int,
        ),
    ]
)

class ComplaintViewSet(viewsets.ModelViewSet):

    permission_classes=[IsAuthenticated]
    def get_queryset(self):
        queryset=Complaint.objects.all()
        status_param=self.request.query_params.get("status")
        category_param=self.request.query_params.get("category")
        user_param=self.request.query_params.get("userId")

        if status_param:
            queryset=queryset.filter(status=status_param)
        if category_param:
            queryset=queryset.filter(category=category_param)   
        if  user_param:
            queryset=queryset.filter(created_by=user_param)    

        if self.action in ["update", "partial_update", "destroy"]:
            queryset = queryset.filter(created_by=self.request.user)

        return queryset    



    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return ComplaintUpdateSerializer
        else:
            return ComplaintSerializer

    def perform_create(self,serializer):
        serializer.save(created_by=self.request.user)
