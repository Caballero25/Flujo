from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from . import forms
from .models import User
# Create your views here.

@login_required
def mainPage(request):
    return render(request, "main.html")


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('mainPage')
    if request.method == "POST":
        username = request.POST.get('userName')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, f'El usuario {username} no existe')
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mainPage')
        else:
            messages.error(request, 'Contraseña incorrecta')

        
    return render(request, 'templates_user/login.html')


def signupPage(request):
    if request.user.is_authenticated:
        return redirect('mainPage')
    if request.method == "POST":
        email = request.POST.get('email')
        username = request.POST.get('userName')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        validEmail = User.objects.filter(email=email).first()
        validUsername = User.objects.filter(username=username).first()
        if validEmail != None: 
            messages.error(request, 'El correo ingresado no está disponible')
        elif validUsername != None: 
            messages.error(request, 'El nombre de usuario no está disponible')
        if password != password2:
            messages.error(request, 'Las contraseñas no coinciden')
        else:
            try:
                newuser = User.objects.create(username=username, email=email)
                newuser.set_password(password)
                newuser.save()
                login(request, newuser)
                return redirect ('mainPage')
            except:
                messages.error(request, 'Revise los errores')
            
        
    return render(request, 'templates_user/signup.html')

@login_required
def logoutPage(request):
    logout(request)
    return redirect('loginPage')

@login_required
def EditPerfilPage(request):
    user = request.user
    form = forms.UserUpdateForm(instance=user)
    if request.method == 'POST':
        form = forms.UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            print(form.data)
            user = form.save()
            return redirect('perfilPage')
        else:
            messages.error(request, 'Ocurrió un error al editar sus datos')
    
    return render(request, 'templates_user/perfil.html', {'form': form, 'user':user})    