from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.db.models.functions import Substr
from django.db.models import Q
from teams.models import Team
from user.models import User
from projects.models import Project
from .models import Task, Comment

@login_required
def getTasks(request, pk):
    try: 
        searchProject = Project.objects.get(id = int(pk))
    except:
        messages.error(request, 'Error de autenticación: no eres miembro del proyecto')
        return redirect("editProject", pk)
    if request.method == "POST":
        responsable = request.POST.get("responsable")
        taskName = request.POST.get("taskName")
        taskGoal = request.POST.get("taskGoal")
        if responsable == "" or taskName == "" or taskGoal =="":
            messages.error(request, 'Todos los campos son obligatorios')
        elif len(taskName) > 100 or len(taskGoal) > 200:
            messages.error(request, 'Límite de carácteres excedido - Nombre: 100 carácteres. | Descripción: 200 carácteres.')
        else:
            try: 
                if searchProject.leader != request.user:
                    messages.error(request, 'Error de autenticación: no eres lider del proyecto')
                    return redirect("editProject", pk)
            except:
                messages.error(request, 'Error de autenticación: no eres lider del proyecto')
                return redirect("editProject", pk)
            try:
                encargado = User.objects.get(id=int(responsable))
                newtask = Task.objects.create(project=searchProject, owner=encargado, name=taskName, goal=taskGoal) 
                newtask.save()
                messages.success(request, 'Tarea creada con éxito')
                return redirect("getTasks", pk)
            except:
                messages.error(request, 'Algo salió mal')
    tasks = Task.objects.filter(project = searchProject)[:3]
    team = searchProject.team
    context = {'tasks': tasks, "project": searchProject, "team": team}      
    return render(request, "templates_tasks/main_tasks.html", context)

@login_required
def allTasks(request, pk):
    try: 
        searchProject = Project.objects.get(id = int(pk))
    except:
        messages.error(request, 'Error de autenticación: no eres miembro del proyecto')
        return redirect("editProject", pk)
    tasks = Task.objects.filter(project=searchProject)
    
    context = {"project": searchProject, "tasks": tasks}
    return render(request, "templates_tasks/all_tasks.html", context)

def infoTask(request, pk):
    try: 
        searchTask = Task.objects.get(id = int(pk))
    except:
        messages.error(request, 'Error de autenticación')
        return redirect("getProjects")
    if request.method == "POST":
        comentario = request.POST.get("comentario")
        newComment = Comment.objects.create(task=searchTask, owner=request.user, comment=comentario)
        newComment.save()
        messages.success(request, 'Comentaste esta tarea.')
        return redirect("taskInfo", pk)
    comentarios = Comment.objects.filter(task=searchTask).order_by("-updated_at").all()
    context = {"task": searchTask, "comments": comentarios}
    return render(request, "templates_tasks/info_tasks.html", context)