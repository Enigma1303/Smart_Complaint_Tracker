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
    urgency_score=models.IntegerField(editable=False)
    
    def __str__(self):
        return f"{self.title} ({self.status})"
    

    def calculate_urgency_score(self):

        score=0
        if self.category ==self.Category.ROAD:
            score+=300
        elif self.category== self.Category.ELECTRICITY:
            score+=500
        elif self.category==self.Category.WATER:
            score+=200

        score+=len(self.description)*2

        return score  

    def save(self,*args,**kwargs):
        self.urgency_score=self.calculate_urgency_score()
        super().save(*args,**kwargs)          
      


