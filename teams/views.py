from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from user.models import User
from .models import Team

# Create your views here.

@login_required
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
    teams = Team.objects.filter(leader=request.user).order_by('-created_at')[:3]  
    context = {'teams': teams}      
    return render(request, "templates_teams/main_teams.html", context)

@login_required
def editTeam(request, pk):
    try:
        searchTeam = Team.objects.get(id=pk)
    except:
        return redirect("getTeams")
    if searchTeam.leader != request.user:
        return redirect("getTeams")
    if request.method == 'POST':
        getTeamName = request.POST.get("teamName")
        getTeamGoal = request.POST.get("teamGoal")
        getActivity = request.POST.get("teamActivity")
        if getTeamName == "" or getTeamGoal == "":
            messages.error(request, 'Los datos no pueden estar vacíos')
        else:
            searchTeam.name = getTeamName
            searchTeam.goal = getTeamGoal
            if getActivity == "True" or getActivity == "False":
                active = True if getActivity == "True" else "False"
                searchTeam.is_active = active
            searchTeam.save()
            return redirect("editTeam", pk)
    opcion1 = {"string": "Activo", "bool": "True"} if searchTeam.is_active == True else {"string": "Inactivo", "bool": "False"}
    opcion2 = {"string": "Inactivo", "bool": "False"} if searchTeam.is_active == True else {"string": "Activo", "bool": "True"}
    context = {'team': searchTeam, "opcion1": opcion1, "opcion2": opcion2}
    return render(request, "templates_teams/edit_team.html", context)
        
    
    
    
    