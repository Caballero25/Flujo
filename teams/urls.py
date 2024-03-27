from django.urls import path
from . import views
#/teams/
urlpatterns = [
    path('', views.getTeams, name="getTeams"),
    path('edit/<str:pk>/', views.editTeam, name="editTeam"),
]