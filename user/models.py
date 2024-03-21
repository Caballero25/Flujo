from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group, Permission
from .managers import UserManager

# Create your models here.


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, max_length=100, blank=False)
    username = models.CharField(max_length=40, unique=True, blank=False)
    password = models.CharField(max_length=100)
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, default='AVATAR_DEFAULT.png')
    create_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    groups = models.ManyToManyField(Group, verbose_name=('groups'), blank=True, related_name='user_groups')
    user_permissions = models.ManyToManyField(
        Permission, verbose_name=('user permissions'), blank=True, related_name='user_user_permissions'
    )
    USERNAME_FIELD ='username'
    is_staff = models.BooleanField(default=False)

    objects = UserManager()
    @classmethod
    def create_user(cls, email, username, password, avatar=None, **extra_fields):
        manager = UserManager  # Obtener el gestor por defecto
        return manager.create_user(email, username, password, avatar, **extra_fields)