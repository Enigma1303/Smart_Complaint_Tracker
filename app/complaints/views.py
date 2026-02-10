from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import (extend_schema,
                                OpenApiParameter, 
                                extend_schema_view,
                                OpenApiTypes)

from rest_framework.filters import OrderingFilter


from .models import Complaint
from .serializers import ComplaintSerializer,ComplaintUpdateSerializer

#logger will automatically use the complaints logger which is at debug level

import logging
logger=logging.getLogger(__name__)

@extend_schema_view(
list=extend_schema(
    parameters=[
        OpenApiParameter(
            name="status",
            description="Filter by complaint status (OPEN, IN_PROGRESS, RESOLVED)",
            required=False,
            type=OpenApiTypes.STR,
            enum=[choice[0] for choice in Complaint.Status.choices]
        ),
        OpenApiParameter(
            name="category",
            description="Filter by complaint category (ROAD, WATER, ELECTRICITY)",
            required=False,
            type=OpenApiTypes.STR,
            enum=[choice[0] for choice in Complaint.Category.choices]
        ),
        OpenApiParameter(
            name="mycomplaints",
            description="Set ID  to get complaints created by the logged-in user",
            required=False,
            type=OpenApiTypes.BOOL,
        ),
        OpenApiParameter(
            name="ordering",
            description="Order by 'created_at' or 'urgency_score'. Prefix with '-' for descending.",
            required=False,
            type=OpenApiTypes.STR,
            enum=[
                   "created_at",
                   "-created_at",
                   "urgency_score",
                "-urgency_score",
    ],
        ),
    ]
)
)

class ComplaintViewSet(viewsets.ModelViewSet):

    permission_classes=[IsAuthenticated]


    filter_backends = [OrderingFilter]
    ordering_fields = ["created_at", "urgency_score"]
    ordering = ["-created_at"]

    def get_queryset(self):
        
        user = self.request.user
        user_id = user.id if getattr(user, "is_authenticated", False) else None
        params = self.request.query_params

        logger.debug(
        "Fetching complaints",
        extra={
            "action": self.action,
            "user_id": user_id,
            "authenticated": getattr(user, "is_authenticated", False),
            "params": dict(params),
        },
    )

        queryset=Complaint.objects.all()
        status_param=self.request.query_params.get("status")
        category_param=self.request.query_params.get("category")
        mycomplaints_param=self.request.query_params.get("mycomplaints")
        

        if status_param:
            queryset=queryset.filter(status=status_param)
        if category_param:
            queryset=queryset.filter(category=category_param)   
        if  mycomplaints_param is not None:
            if mycomplaints_param.lower()=="true":
                queryset=queryset.filter(created_by=self.request.user)
            

        if self.action in ["update", "partial_update", "destroy"]:
            queryset = queryset.filter(created_by=self.request.user)

        return queryset    



    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
             serializer= ComplaintUpdateSerializer
        else:
            serializer= ComplaintSerializer
        
        logger.debug("Serializer selected",
                     extra={
                         "view":self.__class__.__name__,
                         "action":self.action,
                         "serializer":serializer.__name__,
                         "method":self.request.method
                     })
        
        return serializer

    def perform_create(self, serializer):
         try:
          complaint = serializer.save(created_by=self.request.user)
          logger.info(
            f"Complaint created id={complaint.id} category={complaint.category}"
        )
         except Exception as e:
            logger.error(
            "Error while creating complaint",
            exc_info=True
        )
            raise

    