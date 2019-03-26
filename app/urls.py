"""petitions URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("new-petition", views.NewPetitionPage.as_view(), name='new_petition'),
    path("p/<int:pk>", views.petition_details, name='petition_detail'),
    path("logout", views.logout, name='logout'),
    path("login", views.LoginPage.as_view(), name='login'),
    path("signup", views.SignupPage.as_view(), name='signup'),
]
