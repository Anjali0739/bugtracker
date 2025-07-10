from django.db import models

# Create your models here.

class Bug(models.Model):
    STATUS_CHOICES =[
        ("OPEN", "Open"),
        ("IN_PROGRESS", "In Progress"),
        ("RESOLVED", "Resolved"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="OPEN")
    created_by=models.CharField(max_length=100)
    created_at=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.title}-{self.status}"
