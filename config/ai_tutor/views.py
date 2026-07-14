from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
from django.shortcuts import render



@login_required
def ai_tutor_page(request):

    return render(
        request,
        "ai_tutor/ai_tutor.html"
    )

