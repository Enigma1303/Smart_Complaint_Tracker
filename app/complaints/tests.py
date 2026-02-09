from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from complaints.models import Complaint

def create_user(email="test@example.com" , password="testpass123"):
    return get_user_model().objects.create_user(email=email,password=password)

class ComplaintAPITests(APITestCase):
    
    def test_create_complaint(self):
        """
        Test to see if authenticated user can create a complaint
        we check for same title,status being open and 
        created by user being the same and status code as well
        """
        user=create_user()
        self.client.force_authenticate(user=user)

        payload={
            "title":"Water Leakage",
            "description":"Water overflowing out of drains in Rd12",
            "category":"WATER"
        }

        response=self.client.post("/api/complaints/",payload)

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        complaint=Complaint.objects.get(id=response.data["id"])

        self.assertEqual(complaint.title,payload['title'])
        self.assertEqual(complaint.created_by,user)
        self.assertEqual(complaint.status, Complaint.Status.OPEN)
    
    def test_unauthorized_access(self):
        """Test that authentication is required for create""" 
        payload = {
        "title": "Unauthorized complaint",
        "description": "This should not be allowed",
        "category": "ROAD",
        }
        response = self.client.post("/api/complaints/", payload)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_put_complaint(self):
        user=create_user()
        self.client.force_authenticate(user)

        orignalcomplaint=Complaint.objects.create(
          title="Road falling appart cause of PUT",
          description="Some thing happend at PUT",
          category="ROAD",
          created_by=user,
        )
        updatedcomplaint={
            "title":"Water Leakage",
            "description":"Water overflowing out of drains in Rd12",
            "category":"WATER",
            "status":"RESOLVED"
        }
        response=self.client.put(f"/api/complaints/{orignalcomplaint.id}/",updatedcomplaint)


        self.assertEqual(response.status_code,status.HTTP_200_OK)
        orignalcomplaint.refresh_from_db()
        self.assertEqual(orignalcomplaint.category,updatedcomplaint["category"])
        self.assertEqual(orignalcomplaint.status,Complaint.Status.RESOLVED)



    def test_patch_complaint(self):
        user=create_user()
        self.client.force_authenticate(user)

        orignalcomplaint=Complaint.objects.create(
          title="Road falling appart cause of PATCH",
          description="Some thing happend at PATCH",
          category="ROAD",
          created_by=user,
        )
        updatedcomplaint={
            "category":"WATER",
            "status":"RESOLVED"
        }
        response=self.client.patch(f"/api/complaints/{orignalcomplaint.id}/",updatedcomplaint)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
        orignalcomplaint.refresh_from_db()
        self.assertEqual(orignalcomplaint.category,updatedcomplaint["category"])
        self.assertEqual(orignalcomplaint.status,Complaint.Status.RESOLVED)    