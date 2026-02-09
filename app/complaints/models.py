from django.db import models
from django.conf import settings

class Complaint(models.Model):
    
    #define classes for select boxes in choices
    class Category(models.TextChoices):
        ROAD="ROAD","Road"
        WATER="WATER","Water"
        ELECTRICITY="ELECTRICITY","Electricity"

    class Status(models.TextChoices):
        OPEN="OPEN","Open"
        IN_PROGRESS="IN_PROGRESS","In Progress"
        RESOLVED="RESOLVED","Resolved"
            

    title= models.CharField(max_length=255)
    description=models.TextField()
    category=models.CharField(max_length=20,choices=Category)
    status=models.CharField(max_length=20,choices=Status,default=Status.OPEN)
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.title} ({self.status})"
      


