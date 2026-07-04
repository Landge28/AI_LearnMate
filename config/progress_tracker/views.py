from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import ProgressTracker
from quizzes.models import StudentResult
from courses.models import Course


@login_required
def progress_tracker(request):

    progress = ProgressTracker.objects.filter(
        student=request.user
    ).first()

    recent_results = (
        StudentResult.objects
        .filter(student=request.user)
        .select_related("quiz")
        .order_by("-attempted_at")[:5]
    )

    total_courses = Course.objects.count()

    context = {

        "progress": progress,

        "recent_results": recent_results,

        "total_courses": total_courses,

    }

    return render(
        request,
        "progress_tracker/progress_tracker.html",
        context
    )