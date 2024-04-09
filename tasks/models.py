from django.db import models
from user.models import User
from projects.models import Project
# Create your models here.

class Task(models.Model):
    project = models.ForeignKey(Project, null=True, on_delete = models.SET_NULL, related_name="taskteam")
    owner = models.ForeignKey(User , null=True, on_delete = models.SET_NULL, related_name="taskteam")
    name = models.CharField(max_length=100, blank=False, null=False)
    goal = models.TextField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name + " | " + self.goal[0:10]  
    class Meta:
        ordering = ['-created_at']      
        
        
class Comment(models.Model):
    task = models.ForeignKey(Task, null=True, on_delete = models.SET_NULL, related_name="taskcomment")
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)