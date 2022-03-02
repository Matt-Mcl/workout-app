from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response
from django.shortcuts import redirect
from django.contrib import messages

from .helpers import views_helper
from .serializers import *
from .models import *
from .forms import *


@login_required
def WalkFormView(request):

    if request.method == "GET":
        user = User.objects.filter(id=request.user.id)[0]
        # Get walks ordered by newest first
        user_walks = Walk.objects.filter(user=user).order_by("-start_time")

        walk_form = WalkForm()
        return render(request=request, template_name="workouts/walks.html", context={'walk_form': walk_form, 'walks': user_walks})

    elif request.method == "POST":
        user = User.objects.filter(id=request.user.id)[0]
        walk_form = WalkForm(request.POST)
        walk_form.instance.user = user
        if walk_form.is_valid():
            walk_form.save()

        return redirect('/walks/')

    else:
        return Response({f"invalid request"}, status=400)


class WalkAPIView(APIView):
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get(self, request):
        user = views_helper.get_user_data(request)[0]

        user_walks = Walk.objects.filter(user=user)
        if user.is_superuser:
            user_walks = Walk.objects.all()
        serializer = WalkSerializer(user_walks, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        walk = request.data
        walk['user'] = views_helper.get_user_data(request)[0].id

        serializer = WalkSerializer(data=walk, context={'request': request})
        if not serializer.is_valid():
            return Response({f"invalid request"}, status=400)
        status = serializer.save()

        return Response({f"success: \"{status}\" walk created successfully"})


class RunAPIView(APIView):
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get(self, request):
        user = views_helper.get_user_data(request)[0]

        user_runs = Run.objects.filter(user=user)
        if user.is_superuser:
            user_runs = Run.objects.all()
        serializer = RunSerializer(user_runs, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        run = request.data
        run['user'] = views_helper.get_user_data(request)[0].id

        serializer = RunSerializer(data=run, context={'request': request})
        if not serializer.is_valid():
            return Response({f"invalid request"}, status=400)
        status = serializer.save()

        return Response({f"success: \"{status}\" run created successfully"})


class UserAPIView(APIView):
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get(self, request):
        user = views_helper.get_user_data(request)
        if user[0].is_superuser:
            user = User.objects.all()
        serializer = UserSerializer(user, many=True, context={'request': request})
        return Response(serializer.data)


class KeyView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = User.objects.filter(id=request.user.id)[0]

        user_key = APIKey.objects.filter(name=user.username)
        if user.is_superuser:
            user_key = APIKey.objects.all()
        serializer = KeySerializer(user_key, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        user = User.objects.filter(id=request.user.id)[0]

        if APIKey.objects.filter(name=user.username):
            return Response({f"invalid request: user already has an API key"}, status=400)

        api_key, key = APIKey.objects.create_key(name=user.username)

        return Response({
            "success": "key created successfully." ,
            "IMPORTANT": "Note this key down as it will not be shown again",
            "key": key
        })


@login_required
def home(request):
    return render(request, "registration/success.html", {})
 

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username = username, password = password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
