from django.urls import path
from . import views
#/projects/
urlpatterns = [
    path('', views.getProjects, name="getProjects"),
    path('all/', views.allProjects, name="allProjects"),
    path('edit/<str:pk>/', views.editProject, name="editProject"),
    #path('edit/remove/<str:pk>/', views.removeTeamMember, name="removeMember"),
    #path('edit/add/<str:pk>/', views.addTeamMember, name="addMember"),
]