from django.db import models
from user.models import User

# Create your models here.


class Team(models.Model):
    leader = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name="lider")
    members = models.ManyToManyField(User)
    name = models.CharField(max_length=100, blank=False, null=False)
    goal = models.TextField(max_length=200, blank=False, null=False)
    is_active = models.BooleanField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name + " | " + self.goal[0:10]  