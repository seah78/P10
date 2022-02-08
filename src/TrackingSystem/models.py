from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    """ 
    
    """
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=255)
    
    
class Project(models.Model):
    TYPE_BACKEND = "backend"
    TYPE_FRONTEND = "frontend"
    TYPE_IOS = "ios"
    TYPE_CHOICES = [
        (TYPE_BACKEND, "Back-end"),
        (TYPE_FRONTEND, "Front-end"),
        (TYPE_IOS, "iOS"),
    ]

    title = models.CharField(max_length=80)
    description = models.CharField(max_length=550)
    project_type = models.CharField(max_length=8, choices=TYPE_CHOICES)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)