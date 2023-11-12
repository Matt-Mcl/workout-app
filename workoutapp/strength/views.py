from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from .models import *

@login_required()
def StrengthView(request):

    user = User.objects.filter(id=request.user.id)[0]

    workouts = StrengthWorkout.objects.filter(user=user).order_by("-date")

    # print(workouts[0].exercises.all()[0].kg_done)

    return render(
        request=request,
        template_name="strength/strength.html", 
        context={
            "workout": workouts[0]
        }
    )

