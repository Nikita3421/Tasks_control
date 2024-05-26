from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Task(models.Model):
    STATUS_CHOICES = [
        ('todo', 'To Do'),
        ('in_progres', 'In Progres'),
        ('done', 'Done')
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical')
    ]
    title = models.CharField(max_length=511)
    description = models.TextField()
    status = models.CharField(max_length=31, choices=STATUS_CHOICES, default = 'todo')
    priority = models.CharField(max_length=31, choices=PRIORITY_CHOICES, default = 'medium')
    u_date = models.DateTimeField(null=True, blank=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'tasks' )

class Comment(models.Model):
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name= 'comments' )
    created_at = models.DateTimeField(null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name= 'users' )
    media = models.FileField(upload_to='comments_media/' , blank=True, null=True)
