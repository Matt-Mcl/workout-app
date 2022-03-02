"""workoutapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib.auth import views as auth_views

from workouts import views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('walks/', views.WalkFormView, name='walks'),
    path('api/walks/', views.WalkAPIView.as_view(), name='api_walks'),
    path('api/runs/', views.RunAPIView.as_view(), name='api_runs'),
    path('api/users/', views.UserAPIView.as_view(), name='api_runs'),
    path('api/keys/', views.KeyView.as_view(), name='api_keys'),
    path('', views.home, name='home'),
]
