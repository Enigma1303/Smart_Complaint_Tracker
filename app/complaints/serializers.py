from rest_framework import serializers
from .models import Complaint


class ComplaintSerializer(serializers.ModelSerializer):
    """Serializer for all requests except updates"""
    class Meta:
        model = Complaint
        fields = [
            "id",
            "title",
            "description",
            "category",
            "status",
            "created_at",
            "urgency_score"
        ]
        read_only_fields = ["id", "status", "created_at","urgency_score"]

    def create(self,validated_data):
        """Create a complaint"""
        return Complaint.objects.create(**validated_data)  
    
    
class ComplaintUpdateSerializer(serializers.ModelSerializer):
    """serializer for update requests with Status edits enabled"""
    class Meta:
        model = Complaint
        fields = [
            "title",
            "description",
            "category",
            "status",
        ]

    def update(self,instance,validated_data):
        """Update a complaint"""
        for field,value in validated_data.items():
            setattr(instance,field,value)

        instance.save()
        return instance    
