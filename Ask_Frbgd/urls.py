"""Ask_Frbgd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from app import views

urlpatterns = [
    path('ask/', views.AskView.as_view(), name='ask'),
    path('hot/', views.HotView.as_view(), name='hot'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogOutView.as_view(), name='logout'),
    path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('tag/<tag_name>/', views.ListingQView.as_view(), name='tag'),
    path('', views.IndexView.as_view(), name='main'),
]

handler404 = 'app.views.error_404'
