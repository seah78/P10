from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """ 
    user model
    """
    
    first_name = models.CharField(max_length=80)
    last_name = models.CharField(max_length=80)
    email = models.EmailField(max_length=255)
    
    
class Project(models.Model):
    """
    project model
    """
    
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
    
    
class Contributors(models.Model):
    """
    contributor model
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, related_name='contributors', on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    
    
class Issues(models.Model):
    """
    issue model
    """
    
    title = models.CharField(max_length=160)
    description = models.CharField(max_length=550)
    tag = models.CharField(max_length=550)
    priority = models.CharField(max_length=550)
    project = models.ForeignKey(Project, related_name='issues', on_delete=models.CASCADE)
    status= models.CharField(max_length=550)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(User,
                                      on_delete=models.CASCADE,
                                      related_name='assigned_user')
    created_time = models.DateTimeField(auto_now_add=True)
    
    
class Comments(models.Model):

    description = models.CharField(max_length=550)
    author_user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
