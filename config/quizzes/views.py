from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404
from .models import Quiz, Question

from django.db.models import Max, Count
from .models import Quiz, StudentResult
from .models import Quiz

def quiz_detail(request, quiz_id):

    quiz = get_object_or_404(Quiz,id=quiz_id)

    questions = Question.objects.filter(quiz=quiz)

    context = {

        "quiz": quiz,
        "questions": questions,

    }

    return render(request,"quizzes/quiz_detail.html",

        context

    )

def quiz_result(request):

    return render(request,"quizzes/quiz_result.html")






def quiz_list(request):

    quizzes = Quiz.objects.select_related("course").all()

    quiz_data = []

    for quiz in quizzes:

        results = StudentResult.objects.filter(
            student=request.user,
            quiz=quiz
        )

        quiz_data.append({

            "quiz": quiz,

            "attempts": results.count(),

            "best_score": results.aggregate(
                Max("score")
            )["score__max"],

            "completed": results.exists()

        })

    return render(

        request,

        "quizzes/quiz_list.html",

        {

            "quiz_data": quiz_data

        }

    )