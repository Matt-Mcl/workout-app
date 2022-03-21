from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import redirect
from rest_framework.views import APIView
from rest_framework_api_key.models import APIKey
from rest_framework.permissions import IsAuthenticated
from rest_framework_api_key.permissions import HasAPIKey
from rest_framework.response import Response
from datetime import timedelta

from .helpers import views_helper
from .serializers import *
from .models import *
from .forms import *


@login_required
def WorkoutFormView(request):

    if request.method == "GET":
        user = User.objects.filter(id=request.user.id)[0]
        # Get workouts ordered by newest first
        user_workouts = Workout.objects.filter(user=user).order_by("-start_time")

        this_page = request.GET.get("page", 1)
        paginated_workouts = Paginator(user_workouts, 15)

        try:
            page_workouts = paginated_workouts.page(this_page)
        except PageNotAnInteger:
            page_workouts = paginated_workouts.page(1)
        except EmptyPage:
            page_workouts = paginated_workouts.page(paginated_workouts.num_pages)

        workout_form = WorkoutForm()
        return render(request=request, template_name="workouts/workouts.html", context={'workout_form': workout_form, 'workouts': page_workouts})

    elif request.method == "POST":
        user = User.objects.filter(id=request.user.id)[0]
        workout_form = WorkoutForm(request.POST)
        workout_form.instance.user = user
        if workout_form.is_valid():
            workout_form.save()

        return redirect('/workouts/')

    else:
        return HttpResponse(content="invalid request", status=400)


@login_required
def EditWorkout(request, workout_id):
    user = User.objects.filter(id=request.user.id)[0]
    workout = Workout.objects.filter(id=workout_id)[0]

    if request.method == "GET":
        if user == workout.user:
            workout_form = WorkoutForm(instance=workout)
            return render(request=request, template_name="workouts/edit_workout.html", context={'workout_form': workout_form})

        else:
            return HttpResponse(content="invalid request", status=400)
    
    elif request.method == "POST":
        if request.POST.get('delete') and user == workout.user:
            workout.delete()
        else:
            # Retrieve seconds if present
            seconds = timedelta(seconds=workout.start_time.second)
            workout_form = WorkoutForm(request.POST, instance=workout)
            if workout_form.is_valid():
                modified_workout = workout_form.save(commit=False)
                modified_workout.user = user
                # Add seconds back on
                modified_workout.start_time += seconds
                modified_workout.save()

        return redirect('/workouts/')


    else:
        return HttpResponse(content="invalid request", status=400)


class WorkoutAPIView(APIView):
    permission_classes = [HasAPIKey | IsAuthenticated]

    def get(self, request):
        user = views_helper.get_user_data(request)[0]

        user_workouts = Workout.objects.filter(user=user)
        if user.is_superuser:
            user_workouts = Workout.objects.all()
        serializer = WorkoutSerializer(user_workouts, many=True, context={'request': request})
        return Response(serializer.data)
    
    def post(self, request):
        user_id = views_helper.get_user_data(request)[0].id
        status = []

        if "HTTP_AUTO_EXPORT" in request.META:
            workouts = views_helper.parse_json_data(request, user_id)
            for w in workouts:
                serializer = WorkoutSerializer(data=w, context={'request': request})
                if serializer.is_valid():
                    status.append(serializer.save())
            if not status:
                return Response({f"success: no workouts created"})
        else:
            workout = request.data
            workout['user'] = user_id
            serializer = WorkoutSerializer(data=workout, context={'request': request})
            if not serializer.is_valid():
                return Response({f"error: invalid request"}, status=400)
            status = serializer.save()

        return Response({f"success: {status} workout(s) created successfully"})


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
            return Response({f"error: user already has an API key"}, status=400)

        api_key, key = APIKey.objects.create_key(name=user.username)

        return Response({
            "success": "key created successfully." ,
            "IMPORTANT": "Note this key down as it will not be shown again",
            "key": key
        })


@login_required
def home(request):
    return render(request, "registration/success.html")


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
