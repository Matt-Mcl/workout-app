from runpy import run_module
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, get_user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework_api_key.models import APIKey
from rest_framework.response import Response
from .helpers import views_helper

from .serializers import WalkSerializer, RunSerializer, UserSerializer
from .models import Walk, Run, User

class WalkView(APIView):
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
        walk['user'] = get_user(request).id

        serializer = WalkSerializer(data=walk, context={'request': request})
        if not serializer.is_valid():
            return Response({f"invalid request"}, status=400)
        status = serializer.save()

        return Response({f"success: \"{status}\" walk created successfully"})


class RunView(APIView):
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
        run_module['user'] = get_user(request).id

        serializer = RunSerializer(data=run, context={'request': request})
        if not serializer.is_valid():
            return Response({f"invalid request"}, status=400)
        status = serializer.save()

        return Response({f"success: \"{status}\" run created successfully"})


class UserView(APIView):
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get(self, request):
        user = views_helper.get_user_data(request)
        if user[0].is_superuser:
            user = User.objects.all()
        serializer = UserSerializer(user, many=True, context={'request': request})
        return Response(serializer.data)


def walk_detail(request, walk_id):
    try:
        walk = Walk.objects.get(id=walk_id)
    except Walk.DoesNotExist:
        raise Http404('Walk not found')
    return render(request, 'walk_detail.html', {
        'walk': walk,
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


