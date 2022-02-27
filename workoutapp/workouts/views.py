from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import Http404
from rest_framework import viewsets

from .serializers import WalkSerializer, RunSerializer
from .models import Walk, Run


class WalkViewSet(viewsets.ModelViewSet):
    queryset = Walk.objects.all().order_by('distance')
    serializer_class = WalkSerializer


class RunViewSet(viewsets.ModelViewSet):
    queryset = Run.objects.all().order_by('distance')
    serializer_class = RunSerializer


# def home(request):
#     walks = Walk.objects.all()
#     runs = Run.objects.all()
#     return render(request, 'home.html', {
#         'walks': walks,
#         'runs': runs,
#     })


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