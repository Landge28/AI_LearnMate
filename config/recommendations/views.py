from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Recommendation


@login_required
def recommendation_list(request):

    recommendations = Recommendation.objects.select_related(
        "course"
    ).filter(
        student=request.user
    )

    return render(

        request,

        "recommendations/recommendations.html",

        {

            "recommendations": recommendations

        }

    )