from django.urls import path
from . import views
#/tasks/
urlpatterns = [
    path('<str:pk>', views.getTasks, name="getTasks"),
    path('all/<str:pk>/', views.allTasks, name="allTasks"),
    path('info/<str:pk>/', views.infoTask, name="taskInfo"),
    #path('edit/remove/<str:pk>/', views.removeTeamMember, name="removeMember"),
    #path('edit/add/<str:pk>/', views.addTeamMember, name="addMember"),
]