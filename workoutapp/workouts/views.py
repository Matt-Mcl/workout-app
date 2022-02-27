from django.shortcuts import render
from django.http import Http404

from .models import Walk, Run


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

