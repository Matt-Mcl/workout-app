from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response

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
        return HttpResponse(content="invalid request", status=400)


@login_required
def EditWalk(request, walk_id):
    user = User.objects.filter(id=request.user.id)[0]
    walk = Walk.objects.filter(id=walk_id)[0]

    if request.method == "GET":
        if user == walk.user:
            walk_form = WalkForm(instance=walk)
            return render(request=request, template_name="workouts/edit_walk.html", context={'walk_form': walk_form})

        else:
            return HttpResponse(content="invalid request", status=400)
    
    elif request.method == "POST":
        if request.POST.get('delete') and user == walk.user:
            walk.delete()
        else:
            walk_form = WalkForm(request.POST, instance=walk)
            walk_form.instance.user = user
            if walk_form.is_valid():
                walk_form.save()

        return redirect('/walks/')


    else:
        return HttpResponse(content="invalid request", status=400)


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


@login_required
def RunFormView(request):

    if request.method == "GET":
        user = User.objects.filter(id=request.user.id)[0]
        # Get runs ordered by newest first
        user_runs = Run.objects.filter(user=user).order_by("-start_time")

        run_form = RunForm()
        return render(request=request, template_name="workouts/runs.html", context={'run_form': run_form, 'runs': user_runs})

    elif request.method == "POST":
        user = User.objects.filter(id=request.user.id)[0]
        run_form = RunForm(request.POST)
        run_form.instance.user = user
        if run_form.is_valid():
            run_form.save()

        return redirect('/runs/')

    else:
        return HttpResponse(content="invalid request", status=400)


@login_required
def EditRun(request, run_id):
    user = User.objects.filter(id=request.user.id)[0]
    run = Run.objects.filter(id=run_id)[0]

    if request.method == "GET":
        if user == run.user:
            run_form = RunForm(instance=run)
            return render(request=request, template_name="workouts/edit_run.html", context={'run_form': run_form})

        else:
            return HttpResponse(content="invalid request", status=400)
    
    elif request.method == "POST":
        run_form = RunForm(request.POST, instance=run)
        run_form.instance.user = user
        if run_form.is_valid():
            run_form.save()

        return redirect('/runs/')

    else:
        return HttpResponse(content="invalid request", status=400)


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
