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
from django.shortcuts import redirect

from workouts import views as workouts_views
from strength import views as strength_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('strength/', strength_views.StrengthView, name='strength'),
    
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', workouts_views.register, name='register'),
    path('workouts/', workouts_views.WorkoutFormView, name='workout'),
    path('workouts/edit/<int:workout_id>/', workouts_views.EditWorkout, name='edit_workout'),
    path('fitness/<int:weeks>/', workouts_views.FitnessMinsView, name='fitness'),
    path('fitness/', lambda request: redirect('/fitness/24/')),
    path('api/workouts/', workouts_views.WorkoutAPIView.as_view(), name='api_workout'),
    path('api/vo2/', workouts_views.VO2APIView.as_view(), name='api_vo2'),
    path('api/users/', workouts_views.UserAPIView.as_view(), name='api_users'),
    path('api/keys/', workouts_views.KeyView.as_view(), name='api_keys'),
    path('', workouts_views.home, name='home'),
]
