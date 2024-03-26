from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from user.models import User
from .models import Team

# Create your views here.

def getTeams(request):
    if request.method == "POST":
        teamName = request.POST.get("teamName")
        teamGoal = request.POST.get("teamGoal")
        if teamName == "" or teamGoal == "":
            messages.error(request, 'Ambos campos son obligatorios')
        elif len(teamName) > 100 or len(teamGoal) > 200:
            messages.error(request, 'Límite de carácteres excedido - Nombre: 100 carácteres. | Propósito: 200 carácteres.')
        else:
            try:
                newTeam = Team.objects.create(leader=request.user, name=teamName, goal=teamGoal) 
                newTeam.save()
                return redirect("getTeams")
            except:
                messages.error(request, 'Algo salió mal')
    teams = Team.objects.all().order_by('-created_at')[:3]  
    context = {'teams': teams}      
    return render(request, "templates_teams/main_teams.html", context)