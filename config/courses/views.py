from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from .models import Course
from .models import StudyMaterial
from django.shortcuts import get_object_or_404
from quizzes.models import Quiz

from django.shortcuts import get_object_or_404
from .models import StudyMaterial
def course_list(request):

    courses = Course.objects.select_related("category").all()

    return render(
        request,
        "courses/course_list.html",
        {
            "courses": courses
        }
    )



def course_detail(request, pk):

    course = get_object_or_404(Course,pk=pk)

    materials = course.materials.all()

    quizzes = Quiz.objects.filter(course=course)

    context = {

        "course": course,
        "materials": materials,
        "quizzes": quizzes,

    }

    return render(

        request,

        "courses/course_detail.html",

        context

    )




def study_material_list(request):

    materials = StudyMaterial.objects.select_related("course").all()

    return render(
        request,
        "courses/study_material_list.html",
        {
            "materials": materials
        }
    )


def material_detail(request, pk):

    material = get_object_or_404(
        StudyMaterial,
        pk=pk
    )

    return render(
        request,
        "courses/material_detail.html",
        {
            "material": material
        }
    )