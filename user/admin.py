from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import User
from .managers import UserManager



class UserCreationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "username", "password"]

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["username", "email", "password", "avatar"]


class CustomUserAdmin(UserAdmin):
    model = User
    form = UserChangeForm
    add_form = UserCreationForm
    manager = UserManager  # Asignar el manager personalizado
    list_display = ('username', 'email')
    fieldsets = (
        (None, {'fields': ('username', 'email', 'password')}),
        ('Información adicional', {'fields': ('avatar',)}),
        # ... otros campos
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password', 'avatar')
        }),
    )
# unregister the Group model from admin.
admin.site.unregister(Group)
admin.site.register(User, CustomUserAdmin)