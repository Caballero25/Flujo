from django.urls import path
from . import views
#/teams/
urlpatterns = [
    path('', views.getTeams, name="getTeams"),
    path('all/', views.allTeams, name="allTeams"),
    path('edit/<str:pk>/', views.editTeam, name="editTeam"),
    path('edit/remove/<str:pk>/', views.removeTeamMember, name="removeMember"),
    path('edit/add/<str:pk>/', views.addTeamMember, name="addMember"),
]