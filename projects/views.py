from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models.functions import Substr
from django.db.models import Q
from user.models import User
from teams.models import Team
from .models import Project

# Create your views here.

@login_required
def getProjects(request):
    if request.method == "POST":
        projectName = request.POST.get("projectName")
        projectGoal = request.POST.get("projectGoal")
        projectTeam = request.POST.get("projectTeam")
        if projectName == "" or projectGoal == "" or projectTeam =="":
            messages.error(request, 'Todos los campos son obligatorios')
        elif len(projectName) > 100 or len(projectGoal) > 200:
            messages.error(request, 'Límite de carácteres excedido - Nombre: 100 carácteres. | Propósito: 200 carácteres.')
        else:
            try: 
                searchTeam = Team.objects.get(id = int(projectTeam))
                if searchTeam.leader != request.user:
                    messages.error(request, 'Error de autenticación: no eres lider del equipo')
                    return redirect("getProjects")
            except:
                messages.error(request, 'Error de autenticación: no eres lider del equipo')
                return redirect("getProjects")
            try:
                newproject = Project.objects.create(leader=request.user, name=projectName, goal=projectGoal, team=searchTeam) 
                newproject.save()
                messages.success(request, 'Proyecto creado con éxito')
                return redirect("getProjects")
            except:
                messages.error(request, 'Algo salió mal')
    teams = Team.objects.annotate(short_name=Substr('name', 1, 20)).filter(leader=request.user).order_by("-updated_at").all()
    projects = Project.objects.filter(leader=request.user).order_by('-created_at')[:3]  
    context = {'projects': projects, "teams": teams}      
    return render(request, "templates_projects/main_projects.html", context)


@login_required
def editProject(request, pk):
    try:
        searchProject = Project.objects.get(id=pk)
    except: 
        return redirect("getProjects")
    if request.method == 'POST':
        if searchProject.leader != request.user:
            messages.error(request, 'Acceso denegado')
            return redirect("getProjects")
        getProjectName = request.POST.get("projectName")
        getProjectGoal = request.POST.get("projectGoal")
        getTeam = request.POST.get("projectTeam")
        getActivity = request.POST.get("projectActivity")
        getImage = request.FILES.get("projectImage")
        if getProjectName == "" or getProjectGoal == "" or getTeam == "":
            messages.error(request, 'Los datos no pueden estar vacíos')
        else:
            try: 
                searchTeam = Team.objects.get(id = int(getTeam))
                if searchTeam.leader != request.user:
                    messages.error(request, 'Error de autenticación: no eres lider del equipo')
                    return redirect("editProject", pk)
            except:
                messages.error(request, 'Error de autenticación: no eres lider del equipo')
                return redirect("editProject", pk)
            searchProject.name = getProjectName
            searchProject.goal = getProjectGoal
            searchProject.team = searchTeam
            if getImage:
                searchProject.image = getImage
            if getActivity == "True" or getActivity == "False":
                active = True if getActivity == "True" else "False"
                searchProject.is_active = active
            searchProject.save()
            messages.success(request, 'Los datos del proyecto fueron editados')
            return redirect("editProject", pk)
    opcion1 = {"string": "Activo", "bool": "True"} if searchProject.is_active == True else {"string": "Inactivo", "bool": "False"}
    opcion2 = {"string": "Inactivo", "bool": "False"} if searchProject.is_active == True else {"string": "Activo", "bool": "True"}
    shortenedTeamName = "Sin definir" if searchProject.team == None else searchProject.team.name[:20]
    teams = Team.objects.annotate(short_name=Substr('name', 1, 20)).filter(leader=request.user).order_by("-updated_at").all()
    context = {'project': searchProject, "opcion1": opcion1, "opcion2": opcion2, "teamName": shortenedTeamName, "teams": teams}
    return render(request, "templates_projects/edit_project.html", context)



@login_required
def allProjects(request):
    teams = Team.objects.filter(Q(members=request.user) | Q(leader=request.user))
    projects = Project.objects.filter(team__in=teams)
    context = {"projects": projects}
    return render(request, "templates_projects/all_projects.html", context)