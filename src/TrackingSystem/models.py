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
    TYPE_ANDROID = "android"
    TYPE_CHOICES = [
        (TYPE_BACKEND, "Back-end"),
        (TYPE_FRONTEND, "Front-end"),
        (TYPE_IOS, "iOS"),
        (TYPE_ANDROID, "Android"),
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
    project = models.ForeignKey(
        Project, related_name="contributors", on_delete=models.CASCADE
    )
    role = models.CharField(max_length=200)


class Issues(models.Model):
    """
    issue model
    """

    PRIORITY_LOW = "low"
    PRIORITY_MEDIUM = "medium"
    PRIORITY_HIGH = "high"
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, "Low"),
        (PRIORITY_MEDIUM, "Medium"),
        (PRIORITY_HIGH, "High"),
    ]

    TAG_BUG = "bug"
    TAG_IMPROVE = "improve"
    TAG_TASK = "task"
    TAG_CHOICES = [
        (TAG_BUG, "Bug"),
        (TAG_IMPROVE, "Improve"),
        (TAG_TASK, "Task"),
    ]

    STATUS_TODO = "to-do"
    STATUS_INPROGRESS = "in-progress"
    STATUS_COMPLETED = "completed"
    STATUS_CHOICES = [
        (STATUS_TODO, "To-Do"),
        (STATUS_INPROGRESS, "In-Progress"),
        (STATUS_COMPLETED, "Completed"),
    ]

    title = models.CharField(max_length=160)
    description = models.CharField(max_length=550)
    tag = models.CharField(max_length=8, choices=TAG_CHOICES)
    priority = models.CharField(max_length=8, choices=PRIORITY_CHOICES)
    project = models.ForeignKey(
        Project, related_name="issues", on_delete=models.CASCADE
    )
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)
    author = models.ForeignKey(to=User, on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="assigned_user"
    )
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):

    description = models.CharField(max_length=550)
    author_user_id = models.ForeignKey(to=User, on_delete=models.CASCADE)
    issue_id = models.ForeignKey(to=Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
