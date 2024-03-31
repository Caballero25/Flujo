from django.db import models
from user.models import User
from teams.models import Team

# Create your models here.

class Project(models.Model):
    leader = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="projectleader")
    team = models.ForeignKey(Team, null=True, on_delete = models.SET_NULL, related_name="projectteam")
    name = models.CharField(max_length=100, blank=False, null=False)
    goal = models.TextField(max_length=200, blank=False, null=False)
    image = models.ImageField(upload_to='projects', default="projects/PROJECT_DEFAULT.jpg")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name + " | " + self.goal[0:10]  
    class Meta:
        ordering = ['-created_at']      