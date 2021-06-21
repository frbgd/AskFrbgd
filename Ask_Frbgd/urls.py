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
    path('hot/', views.hot, name='hot'),
    path('login/', views.login, name='login'),
    path('question/<int:pk>/', views.QuestionView.as_view(), name='question'),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('tag/<tag_name>/', views.listing_q, name='tag'),
    path('', views.index, name='main'),
]

handler404 = 'app.views.error_404'
