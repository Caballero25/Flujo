from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainPage, name="mainPage"),
    path('login/', views.loginPage, name="loginPage"),
    path('signup/', views.signupPage, name="signupPage"),
    path('logout/', views.logoutPage, name="logoutPage"),
]