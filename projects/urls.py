from django.urls import path
from . import views
#/projects/
urlpatterns = [
    path('', views.getProjects, name="getProjects"),
    path('all/', views.allProjects, name="allProjects"),
    path('edit/<str:pk>/', views.editProject, name="editProject"),
]