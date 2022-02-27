from django.shortcuts import render
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


def home(request):
    walks = Walk.objects.all()
    runs = Run.objects.all()
    return render(request, 'home.html', {
        'walks': walks,
        'runs': runs,
    })


def walk_detail(request, walk_id):
    try:
        walk = Walk.objects.get(id=walk_id)
    except Walk.DoesNotExist:
        raise Http404('Walk not found')
    return render(request, 'walk_detail.html', {
        'walk': walk,
    })
