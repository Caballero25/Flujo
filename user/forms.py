from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import User

class UserUpdateForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'avatar']
        
    username = forms.CharField(widget=forms.TextInput(attrs={"class": ""}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": ""}))
    avatar = forms.ImageField(widget=forms.FileInput(attrs={"class": "imagenPerfil"}))
    def save(self, commit=True):
        user = super().save(commit=False)
        # Renombrar el archivo de avatar para eliminar los espacios
        if 'avatar' in self.changed_data:  # Verifica si el avatar ha sido cambiado
            avatar = self.cleaned_data['avatar']
            if avatar:  # Verifica si se ha proporcionado un archivo
                filename = avatar.name.replace(" ", "_")  # Reemplaza espacios con guiones bajos
                user.avatar.save(filename, avatar, save=False)
        if commit:
            user.save()
        return user