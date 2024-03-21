from django.db import models
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager, models.Manager):
    def create_user(self, email, username, password, avatar, **extra_fields):
        print("user desde admin")
        user = self.model(
            email = email,
            username = username,
            avatar = avatar,
            is_staff = False,
            is_superuser = False,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user


    def _create_super_user(self, username, password, **extra_fields):
        print("superuser 2")
        user = self.model(
            email = 'admin@admin.com',
            username = username,
            is_staff = True,
            is_superuser = True,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self.db)
        return user
    
    def create_superuser(self, username, password, **extra_fields):
        print("superuser 1")
        return self._create_super_user(username, password, **extra_fields)